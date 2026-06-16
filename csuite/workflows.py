#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import inspect
import os
from pathlib import Path

from csuite.argument_parsers import parse_and_validate_args
from cfoldseeker.build_cds_db import run_workflow as cfscds_workflow
from cfoldseeker.main import run_workflow as cfs_workflow
from cfoldseeker.extract_sequences import run_workflow as cfs_extract
from cagecleaner.local_genome_run import LocalGenomeRun
from cagecleaner.local_region_run import LocalRegionRun
from cagecleaner.remote_genome_run import RemoteGenomeRun
from cagecleaner.remote_region_run import RemoteRegionRun
from cblaster.classes import Session
from cblaster.plot import plot_session
from cblaster.plot_clusters import plot_clusters
from cblaster.extract_clusters import extract_clusters as cbl_extract
from cblaster.main import cblaster
from cblaster.database import makedb


LOG = logging.getLogger(__name__)


def setup_workflow(workflow_name: str, categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Setup the selected workflow.
    
    Main workflow setup function that selects the right workflow setup function from the workflow keyword,
    and runs it to get parsed and validated argument values ready to pass on the workflow runner.
    
    Args:
        workflow_name (str): name of the selected workflow
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
    
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    match workflow_name:
        case "local_struc_derep":
            setup = setup_local_struc_derep
        case "remote_struc_derep":
            setup = setup_remote_struc_derep
        case "local_struc":
            setup = setup_local_struc
        case "remote_struc":
            setup = setup_remote_struc
        case "local_seq_derep":
            setup = setup_local_seq_derep
        case "remote_seq_derep":
            setup = setup_remote_seq_derep
        case "local_seq":
            setup = setup_local_seq
        case "remote_seq":
            setup = setup_remote_seq
        case "derep":
            setup = setup_derep
        case "report":
            setup = setup_report
        case "remote_extract":
            setup = setup_remote_extract
        case 'local_extract':
            setup = setup_local_extract
        case _:
            raise ValueError('Unknown workflow name!')
    
    parsed_args = setup(categorised_args)
            
    return parsed_args


def setup_local_struc_derep(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a local structure search with dereplication workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
            
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    cfs_args = categorised_args['CFS']
    cfscds_args = categorised_args['CFSCDS']
    lccl_args = categorised_args['lCCL']
    
    main_temp_folder = main_args.temp
    main_output_folder = main_args.output
    
    # cfoldseeker-cds
    cfscds_args.output = main_output_folder / 'cfoldseeker_cds' / 'cds_db.tsv.gz'
    cfscds_args.temp = main_temp_folder
    cfscds_args.cores = main_args.cores
    cfscds_args.force = main_args.force
    cfscds_args.verbosity = main_args.verbosity
    cfscds_args.no_progress = main_args.no_progress
    
    # cfoldseeker
    cfs_args.output = main_output_folder / 'cfoldseeker'
    cfs_args.cds_db_path = cfscds_args.output
    cfs_args.temp = main_temp_folder
    cfs_args.cores = main_args.cores
    cfs_args.force = main_args.force
    cfs_args.verbosity = main_args.verbosity
    cfs_args.no_progress = main_args.no_progress
    
    # CAGEcleaner
    lccl_args.session = cfs_args.output / 'session.json'
    lccl_args.output = main_output_folder / 'cagecleaner'
    lccl_args.temp = main_temp_folder
    lccl_args.genome_dir = cfscds_args.input
    lccl_args.cores = main_args.cores
    lccl_args.force = main_args.force
    lccl_args.verbosity = main_args.verbosity
    lccl_args.no_progress = main_args.no_progress
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_remote_struc_derep(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a remote structure search with dereplication workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    cfs_args = categorised_args['CFS']
    rccl_args = categorised_args['rCCL']
    
    main_temp_folder = main_args.temp
    main_output_folder = main_args.output
    
    # cfoldseeker
    cfs_args.output = main_output_folder / 'cfoldseeker'
    cfs_args.temp = main_temp_folder
    cfs_args.cores = main_args.cores
    cfs_args.force = main_args.force
    cfs_args.verbosity = main_args.verbosity
    cfs_args.no_progress = main_args.no_progress
    cfs_args.mode = 'remote'
    
    # CAGEcleaner
    rccl_args.session = cfs_args.output / 'session.json'
    rccl_args.output = main_output_folder / 'cagecleaner'
    rccl_args.temp = main_temp_folder
    rccl_args.cores = main_args.cores
    rccl_args.force = main_args.force
    rccl_args.verbosity = main_args.verbosity
    rccl_args.no_progress = main_args.no_progress
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_local_struc(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a local structure search workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    cfs_args = categorised_args['CFS']
    cfscds_args = categorised_args['CFSCDS']
    
    main_temp_folder = main_args.temp
    main_output_folder = main_args.output
    
    # cfoldseeker-cds
    cfscds_args.output = main_output_folder / 'cfoldseeker_cds' / 'cds_db.tsv.gz'
    cfscds_args.temp = main_temp_folder
    cfscds_args.cores = main_args.cores
    cfscds_args.force = main_args.force
    cfscds_args.verbosity = main_args.verbosity
    cfscds_args.no_progress = main_args.no_progress
    
    # cfoldseeker
    cfs_args.output = main_output_folder / 'cfoldseeker'
    cfs_args.cds_db_path = cfscds_args.output
    cfs_args.temp = main_temp_folder
    cfs_args.cores = main_args.cores
    cfs_args.force = main_args.force
    cfs_args.verbosity = main_args.verbosity
    cfs_args.no_progress = main_args.no_progress
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_remote_struc(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a remote structure search workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    cfs_args = categorised_args['CFS']
    
    main_temp_folder = main_args.temp
    main_output_folder = main_args.output
    
    # cfoldseeker
    cfs_args.output = main_output_folder / 'cfoldseeker'
    cfs_args.temp = main_temp_folder
    cfs_args.cores = main_args.cores
    cfs_args.force = main_args.force
    cfs_args.verbosity = main_args.verbosity
    cfs_args.no_progress = main_args.no_progress
    cfs_args.mode = 'remote'
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_local_seq_derep(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a local sequence search with dereplication workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    allowed_suffices = {'.fna', '.fasta', '.fa',
                        '.gb', '.gbk', '.gbff',
                        '.gff', '.gff3',
                        '.gz'
                        }
    
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    cbl_args = categorised_args['CBL']
    cbldb_args = categorised_args['CBLDB']
    lccl_args = categorised_args['lCCL']
    
    main_temp_folder = main_args.temp
    main_output_folder = main_args.output
    cblaster_output_folder = main_output_folder / 'cblaster'
    cbldb_db_prefix = main_output_folder / 'cblaster_makedb' / 'local_db'
    
    # cblaster makedb
    # catch a FileNotFoundError if the genome folder does not exist; cannot be postponed until validation time
    try:
        cbldb_args.paths = [str(p) for p in cbldb_args.paths.iterdir() if set(p.suffixes) < allowed_suffices]
    except FileNotFoundError:
        msg = f'Genome folder not found: {cbldb_args.paths}'
        LOG.critical(msg)
        raise FileNotFoundError(msg)
    cbldb_args.database = str(cbldb_db_prefix)
    cbldb_args.force = main_args.force
    cbldb_args.cpus = main_args.cores
    
    # cblaster search
    cbl_args.mode = 'local'
    cbl_args.cpus = main_args.cores
    cbl_args.force = main_args.force
    cbl_args.output = os.devnull
    cbl_args.query_file = str(cbl_args.query_file)
    cbl_args.session_file = [str(cblaster_output_folder / 'session.json')] # cblaster expects this in a list
    cbl_args.blast_file = str(cblaster_output_folder / 'blast.txt')
    cbl_args.databases = [str(cbldb_db_prefix.with_suffix('.dmnd'))] # cblaster expects this in a list
    
    # CAGEcleaner
    lccl_args.session = Path(cbl_args.session_file[0])
    lccl_args.output = main_output_folder / 'cagecleaner'
    lccl_args.temp = main_temp_folder
    lccl_args.genome_dir = Path(cbldb_args.paths[0]).parent
    lccl_args.cores = main_args.cores
    lccl_args.force = main_args.force
    lccl_args.verbosity = main_args.verbosity
    lccl_args.no_progress = main_args.no_progress
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_remote_seq_derep(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a remote sequence search with dereplication workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    cbl_args = categorised_args['CBL']
    rccl_args = categorised_args['rCCL']
    
    main_output_folder = main_args.output / 'cblaster'
    main_temp_folder = main_args.temp
    
    # cblaster search
    cbl_args.mode = 'remote'
    cbl_args.cpus = main_args.cores
    cbl_args.force = main_args.force
    cbl_args.output = os.devnull
    cbl_args.query_file = str(cbl_args.query_file)
    cbl_args.session_file = [str(main_output_folder / 'session.json')] # cblaster expects this in a list
    cbl_args.blast_file = str(main_output_folder / 'blast.txt')
    
    # CAGEcleaner
    rccl_args.session = Path(cbl_args.session_file[0])
    rccl_args.output = main_output_folder / 'cagecleaner'
    rccl_args.temp = main_temp_folder
    rccl_args.cores = main_args.cores
    rccl_args.force = main_args.force
    rccl_args.verbosity = main_args.verbosity
    rccl_args.no_progress = main_args.no_progress
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_local_seq(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a local sequence search workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    allowed_suffices = {'.fna', '.fasta', '.fa',
                        '.gb', '.gbk', 'gbff',
                        '.gff', '.gff3',
                        '.gz'
                        }
    
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    cbl_args = categorised_args['CBL']
    cbldb_args = categorised_args['CBLDB']
    
    main_output_folder = main_args.output / 'cblaster'
    cbldb_db_prefix = main_args.output / 'cblaster_makedb' / 'local_db'
    
    # cblaster makedb
    # catch a FileNotFoundError if genome folder does not exist; cannot be postponed until validation time
    try:
        cbldb_args.paths = [str(p) for p in cbldb_args.paths.iterdir() if set(p.suffixes) < allowed_suffices]
    except FileNotFoundError:
        msg = f'Genome folder not found: {cbldb_args.paths}'
        LOG.critical(msg)
        raise FileNotFoundError(msg)
    cbldb_args.database = str(cbldb_db_prefix)
    cbldb_args.force = main_args.force
    cbldb_args.cpus = main_args.cores
    
    # cblaster search
    cbl_args.mode = 'local'
    cbl_args.cpus = main_args.cores
    cbl_args.force = main_args.force
    cbl_args.output = os.devnull
    cbl_args.query_file = str(cbl_args.query_file)
    cbl_args.session_file = [str(main_output_folder / 'session.json')] # cblaster expects this in a list
    cbl_args.blast_file = str(main_output_folder / 'blast.txt')
    cbl_args.databases = [str(cbldb_db_prefix.with_suffix('.dmnd'))] # cblaster expects this in a list
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_remote_seq(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a remote sequence search workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    cbl_args = categorised_args['CBL']
    
    main_output_folder = main_args.output / 'cblaster'
    
    # cblaster search
    cbl_args.mode = 'remote'
    cbl_args.cpus = main_args.cores
    cbl_args.force = main_args.force
    cbl_args.output = os.devnull
    cbl_args.query_file = str(cbl_args.query_file)
    cbl_args.session_file = [str(main_output_folder / 'session.json')] # cblaster expects this in a list
    cbl_args.blast_file = str(main_output_folder / 'blast.txt')
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_derep(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a dereplication workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    ccl_args = categorised_args['CCL']
    
    main_temp_folder = main_args.temp
    main_output_folder = main_args.output
    
    # CAGEcleaner
    ccl_args.output = main_output_folder / 'cagecleaner'
    ccl_args.temp = main_temp_folder
    ccl_args.cores = main_args.cores
    ccl_args.force = main_args.force
    ccl_args.verbosity = main_args.verbosity
    ccl_args.no_progress = main_args.no_progress
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_report(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a report generation workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    out_args = categorised_args['OUT']
    
    main_temp_folder = main_args.temp
    main_output_folder = main_args.output
    
    # output flags
    out_args.output = main_output_folder
    out_args.temp = main_temp_folder
    out_args.force = main_args.force
    out_args.verbosity = main_args.verbosity
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_remote_extract(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a remote cluster extraction workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    rext_args = categorised_args['rEXT']
    
    main_output_folder = main_args.output
    
    # output flags
    rext_args.output_dir = main_output_folder
    rext_args.force = main_args.force
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_local_extract(categorised_args: dict[argparse.Namespace]) -> dict:
    """
    Set up a local cluster extraction workflow.
    
    Sets shared arguments, and connects input and output file paths passed on by the different tools of the workflow.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow. Typical output of categorise_args() of the argument_parsers module.
            
    Returns:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
                        
    Mutates:
        categorised_args: Argument values are updated to connect the several inputs and outputs between tools.
    """
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    lext_args = categorised_args['lEXT']
    
    main_output_folder = main_args.output
    
    # output flags
    lext_args.output_dir = main_output_folder
    lext_args.cores = main_args.cores
    lext_args.force = main_args.force
    lext_args.verbosity = main_args.verbosity
    lext_args.no_progress = main_args.no_progress
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args
    

def run_workflow(workflow_name: str, parsed_args: dict) -> None:
    """
    Run the workflow using the prepared arguments.
    
    Main workflow runner function that calls the runner selected from the workflow keyword.
    
    Args:
        workflow_name (str): Name of the selected workflow.
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
            
    Returns:
        None
    """
    match workflow_name:
        case 'local_struc_derep':
            run = run_local_struc_derep_workflow
        case 'local_struc':
            run = run_local_struc_workflow
        case 'remote_struc_derep':
            run = run_remote_struc_derep_workflow
        case 'remote_struc':
            run = run_remote_struc_workflow
        case 'derep':
            run = run_derep_workflow
        case 'report':
            run = run_report_workflow
        case 'remote_seq':
            run = run_remote_seq_workflow
        case 'remote_seq_derep':
            run = run_remote_seq_derep_workflow
        case 'local_seq':
            run = run_local_seq_workflow
        case 'local_seq_derep':
            run = run_local_seq_derep_workflow
        case 'remote_extract':
            run = run_remote_extract_workflow
        case 'local_extract':
            run = run_local_extract_workflow
        case _:
            raise ValueError('Unknown workflow name!')
        
    run(parsed_args)


def run_local_struc_derep_workflow(parsed_args: dict) -> None:
    """
    Run the local structure search with dereplication workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    # Build CDS DB
    cfscds_workflow(parsed_args['CFSCDS'])
    
    # Run cfoldseeker
    cfs_workflow(parsed_args['CFS'])
    
    # Run CAGEcleaner in local mode
    lccl_method = parsed_args['lCCL']['method']
    match lccl_method:
        case 'genomes':
            ccl_run = LocalGenomeRun(parsed_args['lCCL'])
        case 'regions':
            ccl_run = LocalRegionRun(parsed_args['lCCL'])
        case _:
            raise ValueError('Invalid local CAGEcleaner mode!')
    
    ccl_run.run()
    
    return None


def run_remote_struc_derep_workflow(parsed_args: dict) -> None:
    """
    Run the remote structure search with dereplication workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    # Run cfoldseeker
    cfs_workflow(parsed_args['CFS'])
    
    # Run CAGEcleaner in local mode
    rccl_method = parsed_args['rCCL']['method']
    match rccl_method:
        case 'genomes':
            ccl_run = RemoteGenomeRun(parsed_args['rCCL'])
        case 'regions':
            ccl_run = RemoteRegionRun(parsed_args['rCCL'])
        case _:
            raise ValueError('Invalid local CAGEcleaner mode!')
    
    ccl_run.run()
    
    return None


def run_local_struc_workflow(parsed_args: dict) -> None:
    """
    Run the local structure search workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    # Build CDS DB
    cfscds_workflow(parsed_args['CFSCDS'])
    
    # Run cfoldseeker
    cfs_workflow(parsed_args['CFS'])
    
    return None


def run_remote_struc_workflow(parsed_args: dict) -> None:
    """
    Run the remote structure search workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    # Run cfoldseeker
    cfs_workflow(parsed_args['CFS'])
    
    return None


def run_remote_seq_workflow(parsed_args: dict) -> None:
    """
    Run the remote sequence search workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    cbl_args = parsed_args['CBL']
    
    # Get the arguments we need for cblaster search
    cbl_func_sig = inspect.signature(cblaster)
    filtered_args = {k: v for k,v in cbl_args.items() if k in cbl_func_sig.parameters}
    
    # Run cblaster search
    cblaster(**filtered_args)
    
    return None
    
    
def run_local_seq_workflow(parsed_args: dict) -> None:
    """
    Run the local sequence search workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    cbl_args = parsed_args['CBL']
    cbldb_args = parsed_args['CBLDB']
    
    # cblaster makedb
    makedb(**cbldb_args)
    
    # Get the arguments we need for cblaster search
    cbl_func_sig = inspect.signature(cblaster)
    filtered_cbl_args = {k: v for k,v in cbl_args.items() if k in cbl_func_sig.parameters}
    
    # cblaster search
    cblaster(**filtered_cbl_args)
    
    return None


def run_local_seq_derep_workflow(parsed_args: dict) -> None:
    """
    Run the local sequence search with dereplication workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    cbl_args = parsed_args['CBL']
    cbldb_args = parsed_args['CBLDB']
    lccl_args = parsed_args['lCCL']
    
    # cblaster makedb
    makedb(**cbldb_args)
    
    # Get the arguments we need for cblaster search
    cbl_func_sig = inspect.signature(cblaster)
    filtered_cbl_args = {k: v for k,v in cbl_args.items() if k in cbl_func_sig.parameters}
    
    # cblaster search
    cblaster(**filtered_cbl_args)
    
    # Run CAGEcleaner in local mode
    lccl_method = lccl_args['method']
    match lccl_method:
        case 'genomes':
            ccl_run = LocalGenomeRun(lccl_args)
        case 'regions':
            ccl_run = LocalRegionRun(lccl_args)
        case _:
            raise ValueError('Invalid local CAGEcleaner mode!')
    
    ccl_run.run()
    
    return None


def run_remote_seq_derep_workflow(parsed_args: dict) -> None:
    """
    Run the remote sequence search with dereplication workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    cbl_args = parsed_args['CBL']
    rccl_args = parsed_args['rCCL']
    
    # Get the arguments we need for cblaster search
    cbl_func_sig = inspect.signature(cblaster)
    filtered_args = {k: v for k,v in cbl_args.items() if k in cbl_func_sig.parameters}
    
    # Run cblaster search
    cblaster(**filtered_args)
    
    # Run CAGEcleaner in local mode
    rccl_method = rccl_args['method']
    match rccl_method:
        case 'genomes':
            ccl_run = RemoteGenomeRun(rccl_args)
        case 'regions':
            ccl_run = RemoteRegionRun(rccl_args)
        case _:
            raise ValueError('Invalid local CAGEcleaner mode!')
    
    ccl_run.run()
    
    return None


def run_derep_workflow(parsed_args: dict) -> None:
    """
    Run the dereplication workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    ccl_args = parsed_args['CCL']
    
    # Run CAGEcleaner
    source = Session.from_file(ccl_args['session']).params['mode']
    method = ccl_args['method']
    mode = (source, method)
    match mode:
        case ('remote', 'genomes'):
            LOG.info('Entering remote genome mode')
            ccl_run = RemoteGenomeRun(ccl_args)
        case ('remote', 'regions'):
            LOG.info('Entering remote region mode')
            ccl_run = RemoteRegionRun(ccl_args)
        case ('local', 'genomes') | ('hmm', 'genomes'):
            LOG.info('Entering local genome mode')
            ccl_run = LocalGenomeRun(ccl_args)
        case ('local', 'regions') | ('hmm', 'regions'):
            LOG.info('Entering local region mode')
            ccl_run = LocalRegionRun(ccl_args)
            
    ccl_run.run()
    
    return None


def run_report_workflow(parsed_args: dict) -> None:
    """
    Run the report generation workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    out_args = parsed_args['OUT']
    
    LOG.info("Reading cblaster session")
    session = Session.from_file(out_args['session'])
    
    if out_args['output_summary']:
        LOG.info("Writing cblaster summary file")
        path = out_args['output'] / 'summary.txt'
        with open(path, 'w') as handle:
            session.format(form = "summary", fp = handle)
        LOG.debug(f'cblaster summary file written at {str(path)}')
        
    if out_args['output_binary']:
        LOG.info("Writing cblaster binary table")
        path = out_args['output'] / 'binary.txt'
        with open(path, 'w') as handle:
            session.format(form = "binary", fp = handle, delimiter = "\t", sort_clusters = True)
        LOG.debug(f'cblaster binary table written at {str(path)}')
    
    if out_args['output_plot']:
        LOG.info("Writing cblaster plot")
        path = out_args['output'] / 'plot.html'
        plot_session(session, output = path)
        LOG.debug(f'cblaster plot written at {str(path)}')
    
    if out_args['output_clinker']:
        LOG.info("Writing clinker plot")
        path = out_args['output'] / "clinker.html"
        plot_clusters(out_args['session'], plot_outfile = path, max_clusters = None)
        LOG.debug(f'clinker plot written at {str(path)}')
        
    return None


def run_remote_extract_workflow(parsed_args: dict) -> None:
    """
    Run the remote cluster extraction workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    rext_args = parsed_args['rEXT']
    
    # Get the arguments we need for cblaster's extract_clusters
    cblext_func_sig = inspect.signature(cbl_extract)
    filtered_cblext_args = {k: v for k,v in rext_args.items() if k in cblext_func_sig.parameters}
    
    # Run cblaster's extract_clusters workflow
    cbl_extract(**filtered_cblext_args)
    
    return None


def run_local_extract_workflow(parsed_args: dict) -> None:
    """
    Run the local cluster extraction workflow.
    
    Distributes the ready-to-use arguments over the appropriate tools and runs them in the right order.
    
    Args:
        parsed_args (dict): dictionary of dictionaries of argument name-value pairs, grouped by tool involved in a workflow.
        
    Returns:
        None
    """
    lext_args = parsed_args['lEXT']
    
    cfs_extract(lext_args)
            
    return None

