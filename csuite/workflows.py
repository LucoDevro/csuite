#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging

from csuite.argument_parsers import parse_and_validate_args
from cfoldseeker.build_cds_db import run_workflow as cfscds_workflow
from cfoldseeker.main import run_workflow as cfs_workflow
from cagecleaner.local_genome_run import LocalGenomeRun
from cagecleaner.local_region_run import LocalRegionRun
from cagecleaner.remote_genome_run import RemoteGenomeRun
from cagecleaner.remote_region_run import RemoteRegionRun


LOG = logging.getLogger(__name__)


def setup_workflow(workflow_name: str, categorised_args: dict[argparse.Namespace]) -> dict:
    match workflow_name:
        case "local_structure_derep":
            parsed_args = setup_local_structure_derep(categorised_args)
        case "structure":
            setup_structure(categorised_args)
        case "sequence_derep":
            setup_sequence_derep(categorised_args)
        case "sequence":
            setup_sequence(categorised_args)
        case "derep":
            setup_derep(categorised_args)
        case _:
            raise ValueError('Unknown workflow name!')
            
    return parsed_args


def setup_local_structure_derep(categorised_args: dict[argparse.Namespace]) -> dict:
    
    ## First connect the I/O arguments of the several tools
    main_args = categorised_args['MAIN']
    cfs_args = categorised_args['CFS']
    cfscds_args = categorised_args['CFSCDS']
    lccl_args = categorised_args['lCCL']
    
    main_temp_folder = main_args.temp
    main_output_folder = main_args.output
    
    # cfoldseeker-cds
    cfscds_args.output = main_output_folder / 'cfoldseeker_cds' / 'cds_db.tsv.gz'
    cfscds_args.force = main_args.force
    cfscds_args.verbosity = main_args.verbosity
    
    # cfoldseeker
    cfs_args.output = main_output_folder / 'cfoldseeker'
    cfs_args.cds_db_path = cfscds_args.output
    cfs_args.temp = main_temp_folder
    cfs_args.force = main_args.force
    cfs_args.verbosity = main_args.verbosity
    
    # CAGEcleaner
    lccl_args.session = cfs_args.output / 'session.json'
    lccl_args.output = main_output_folder / 'cagecleaner'
    lccl_args.temp = main_temp_folder
    lccl_args.force = main_args.force
    lccl_args.verbosity = main_args.verbosity
    
    ## Then parse and validate the argument values
    parsed_args = parse_and_validate_args(categorised_args)
    
    return parsed_args


def setup_structure(categorised_args: dict[argparse.Namespace]) -> dict[argparse.Namespace]:
    pass


def setup_sequence_derep(categorised_args: dict[argparse.Namespace]) -> dict[argparse.Namespace]:
    pass


def setup_sequence(categorised_args: dict[argparse.Namespace]) -> dict[argparse.Namespace]:
    pass


def setup_derep(categorised_args: dict[argparse.Namespace]) -> dict[argparse.Namespace]:
    pass


def run_workflow(workflow_name: str, parsed_args: dict) -> None:
    match workflow_name:
        case 'local_structure_derep':
            run_local_structure_derep_workflow(parsed_args)
        case _:
            raise ValueError('Unknown workflow name!')


def run_local_structure_derep_workflow(parsed_args: dict) -> None:
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


