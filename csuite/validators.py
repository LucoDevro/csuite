#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import tempfile
import argparse
from pathlib import Path
from Bio import SeqIO

from cblaster.parsers import NCBI_DATABASES
from cfoldseeker.extract_sequences import parse_and_validate_arguments as cfsext_arg_validator


LOG = logging.getLogger(__name__)


def validate_main_args(args: argparse.Namespace) -> dict:
    """
    Validate the main shared arguments.
    
    Args:
        args (argparse.Namespace): Argument namespace to be validated and parsed.
        
    Returns:
        parsed_args (dict): dictionary of argument name-value pairs
    """
    # Output directory should not exist yet, unless flagged.
    try:
        args.output.mkdir(parents = True)
    except FileExistsError as err:
        if args.force:
            LOG.warning('Output folder already exists, but it will be overwritten.')
        else:
            LOG.error('Output folder already exists! Rerun with -f to overwrite it.')
            raise err
            
    # Temporary directory should not exist yet if not default, unless flagged.
    if args.temp != Path(tempfile.gettempdir()):
        try:
            args.temp.mkdir(parents = True)
        except FileExistsError as err:
            if args.force:
                LOG.warning('Temp folder already exists, but it will be overwritten.')
            else:
                LOG.error('Temp folder already exists! Rerun with -f to overwrite it.')
                raise err
    args.temp = Path(tempfile.mkdtemp(dir = args.temp))
    
    # Parse and return
    return vars(args)


def validate_report_args(args: argparse.Namespace) -> dict:
    """
    Validate the arguments of the report generation module.
    
    Args:
        args (argparse.Namespace): Argument namespace to be validated and parsed.
        
    Returns:
        parsed_args (dict): dictionary of argument name-value pairs
    """
    # Session file should exist
    if not Path(args.session).is_file():
        raise FileNotFoundError("Session file not found!")
        
    # Parse and return
    return vars(args)


def validate_cblaster_search_args(args: argparse.Namespace) -> dict:
    """
    Validate the arguments of the cblaster search module.
    
    Args:
        args (argparse.Namespace): Argument namespace to be validated and parsed.
        
    Returns:
        parsed_args (dict): dictionary of argument name-value pairs
    """
    # Set filepaths temporarily
    query_file = Path(args.query_file)
    session_file = Path(args.session_file[0])
    
    # Validation checks
    if not query_file.exists():
        raise ValueError('Query file does not exist!')
    if not(args.cpus > 0):
        raise ValueError('Number of cores must be strictly positive.')
    if not(args.max_evalue <= 1 and args.max_evalue > 0): 
        raise ValueError('Maximum e-value should be a number between 0 and 1.')
    if not(args.min_identity >= 0 and args.min_identity <= 100):
        raise ValueError("Minimum sequence identity should be a percentage between 0 and 100.")
    if not(args.min_coverage >= 0 and args.min_coverage <= 100):
        raise ValueError("Minimum query coverage should be a percentage between 0 and 100.")
    if not(args.gap >= 0): 
        raise ValueError("Maximum intergenic gap should be a positive number.")
    if not(args.min_hits >= 1): 
        raise ValueError("Minimum number of hits in a cluster should be strictly positive.")
    if not(args.unique >= 1): 
        raise ValueError("Minimum number of covered queries in a cluster should be strictly positive.")
    if not(args.percentage >= 0 and args.percentage <= 100):
        raise ValueError("Required percentage of query genes should be a percentage between 0 and 100.")
    # Database is mode-dependent
    match args.mode:
        case 'remote':
            if not(set(args.databases) <= set(NCBI_DATABASES)):
                raise ValueError(f"Invalid target database choice. Possible choices: {', '.join(NCBI_DATABASES)}")
        case 'local':
            # Database has not been created yet at this stage
            # And the parent folder is being validated by the makedb validator
            # So there's nothing left to validate in this case
            pass
        case _:
            raise ValueError('Invalid sequence search mode! Possible choices: "remote", "local".')
        
    # Check that required genes are present in the query fasta
    with open(query_file, 'r') as handle:
        queries = SeqIO.to_dict(SeqIO.parse(handle, format = 'fasta'))
        query_headers = set(queries.keys())
    if not(set(args.require) <= query_headers):
        raise ValueError("A required query cannot be found in your query fasta folder. Please check your labels.")
    
    # Output folder can already exist if force flag is on
    try:
        session_file.parent.mkdir(parents = True)
    except FileExistsError as err:
        if args.force:
            LOG.warning('Output folder already exists, but it will be overwritten.')
        else:
            msg = 'Output folder already exists! Rerun with -f to overwrite it.'
            LOG.error(msg)
            raise err
            
    # Session file cannot exist yet.
    # If it's there and force flag is on, remove it.
    if session_file.is_file():
        if args.force:
            LOG.warning('Session file already exists, but it will be overwritten.')
            session_file.unlink()
        else:
            msg = 'Session file already exists! Rerun with -f to overwrite it.'
            LOG.error(msg)
            raise FileExistsError(msg)
            
    # Parse and return
    return vars(args)


def validate_cblaster_makedb_args(args: argparse.Namespace) -> dict:
    """
    Validate the arguments of the cblaster makedb module.
    
    Args:
        args (argparse.Namespace): Argument namespace to be validated and parsed.
        
    Returns:
        parsed_args (dict): dictionary of argument name-value pairs
    """
    if not(args.cpus > 0):
        raise ValueError('Number of cores must be strictly positive.')
    
    # Output directory can already exist if force flag is on
    try:
        Path(args.database).parent.mkdir(parents = True) # Parent since this is a prefix
    except FileExistsError as err:
        if args.force:
            LOG.warning('Output folder already exists, but it will be overwritten.')
        else:
            msg = 'Output folder already exists! Rerun with -f to overwrite it.'
            LOG.error(msg)
            raise err
    
    # Parse and return
    return vars(args)


def validate_remote_extract_args(args: argparse.Namespace) -> dict:
    """
    Validate the arguments of the remote cluster extraction module.
    
    Args:
        args (argparse.Namespace): Argument namespace to be validated and parsed.
        
    Returns:
        parsed_args (dict): dictionary of argument name-value pairs
    """
    try:
        if not args.session.is_file():
            raise IOError('Session file does not exist.')
        if args.max_clusters and not(int(args.max_clusters) > 0):
            raise ValueError('Maximum number of clusters must be a strictly positive integer.')
        if args.score_threshold and not(float(args.score_threshold) > 0):
            raise ValueError('Score threshold must be a strictly positive integer.')
    except (IOError, ValueError) as err:
        raise err
        
    # Parse and return
    return vars(args)


def validate_local_extract_args(args: argparse.Namespace) -> dict:
    """
    Validate the arguments of the remote cluster extraction module.
    
    Args:
        args (argparse.Namespace): Argument namespace to be validated and parsed.
        
    Returns:
        parsed_args (dict): dictionary of argument name-value pairs
        
    Note:
        This validator automatically differentiates between cblaster and cfoldseeker sessions,
            and calls the appropriate validator.
    """
    try:
        if not args.session.is_file():
            raise IOError('Session file does not exist.')
        # Recognise which tool generated this session
        # cblaster leaves the sequence attribute of local searches empty; cfoldseeker fills it with the local filelabel
        session = Session.from_file(args.session)
        first_scaffold = list(session.organisms[0].scaffolds.values())[0]
        match first_scaffold.subjects[0].sequence:
            # cblaster session
            case None:
                parsed_args = validate_remote_extract_args(args)
            # cfoldseeker session
            case str():
                parsed_args = cfsext_arg_validator(args)
            case _:
                raise ValueError('Could not determine session type!')
    except:
        raise
        
    return parsed_args

