#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
from importlib.metadata import version

from csuite.cli_parsers import (register_local_struc_derep_subparser,
                                register_local_struc_subparser,
                                register_remote_struc_derep_subparser,
                                register_remote_struc_subparser,
                                register_derep_subparser,
                                register_report_subparser,
                                register_remote_seq_subparser,
                                register_remote_seq_derep_subparser,
                                register_local_seq_subparser,
                                register_local_seq_derep_subparser,
                                register_remote_extract_subparser,
                                register_local_extract_subparser
                                )
from csuite.argument_parsers import categorise_args
from csuite.workflows import setup_workflow, run_workflow


__version__ = version('csuite')

# Setup default logger configuration
logging.basicConfig(
    level = logging.INFO,
    format = "[%(asctime)s] %(levelname)s [%(name)s: %(funcName)s] - %(message)s",
    datefmt="%H:%M:%S",
    handlers = [logging.StreamHandler(sys.stdout)],
    )
LOG = logging.getLogger(__name__)


def create_main_parser():
    """
    Create the main CLI parser.
    
    Defines the root csuite CLI, and defines the subparsers for each workflow.
    
    Returns:
        parser (argparse.ArgumentParser): Parser object with every subcommand registered and defined.
        
    Note:
        Subcommand parsers are defined in the cli_parsers module.
    """
    parser = argparse.ArgumentParser(
        prog = 'csuite',
                epilog = 
                """
                Lucas De Vrieze
                (c) 2026 Masschelein lab, VIB
                """,
                formatter_class = argparse.RawDescriptionHelpFormatter,
                description = 
                """
                csuite: Streamlined workflows for sequence and structure similarity-based gene cluster mining
                """,
                add_help = False
                )
    
    parser.add_argument('-v', '--version', action = "version", version = "%(prog)s " + __version__)
    parser.add_argument('-h', '--help', action = 'help', help = "Show this help message and exit")
    
    subparsers = parser.add_subparsers(title = 'workflows', dest = 'command')
    
    # local structure with dereplication
    register_local_struc_derep_subparser(subparsers)
    
    # local structure
    register_local_struc_subparser(subparsers)
    
    # remote structure with dereplication
    register_remote_struc_derep_subparser(subparsers)
    
    # remote structure
    register_remote_struc_subparser(subparsers)
    
    # local sequence with dereplication
    register_local_seq_derep_subparser(subparsers)
    
    # local sequence
    register_local_seq_subparser(subparsers)
    
    # remote sequence with dereplication
    register_remote_seq_derep_subparser(subparsers)
    
    # remote sequence
    register_remote_seq_subparser(subparsers)
    
    # dereplication only
    register_derep_subparser(subparsers)
    
    # report generation only
    register_report_subparser(subparsers)
    
    # extract sequences from a remote search
    register_remote_extract_subparser(subparsers)
    
    # extract sequences from a local search
    register_local_extract_subparser(subparsers)
    
    return parser


def setup_logging(verbosity: int) -> None:
    """
    Set up the root logger, overruling any previously set config.
    
    Forces a new basicConfig with an updated verbosity level
    
    Args:
        verbosity (int): Verbosity level (choices: 0,1,2,3,4).
        
    Returns:
        None
    """
    log_levels = {0: logging.CRITICAL,
                  1: logging.ERROR,
                  2: logging.WARNING,
                  3: logging.INFO,
                  4: logging.DEBUG
                  }
    
    logging.basicConfig(
        level = log_levels[verbosity],
        format = "[%(asctime)s] %(levelname)s [%(name)s: %(funcName)s] - %(message)s",
        datefmt="%H:%M:%S",
        handlers = [logging.StreamHandler(sys.stdout)],
        force = True,
        )
    
    return None


def main():
    # Collect args
    parser = create_main_parser()
    args = parser.parse_args()
    workflow_name = args.command
    
    # Categorise them by tool
    categorised_args = categorise_args(args)
    
    # Reconfigure logger with parsed verbosity level
    verbosity = getattr(categorised_args['MAIN'], 'verbosity', 3)
    setup_logging(verbosity)
    
    # Set up the workflow by setting the right I/O arguments
    # Validate arguments on-the-fly, catching and ignoring non-existing 
    # intermediate files for now (will be taken care of by the workflow)
    workflow_args = setup_workflow(workflow_name, categorised_args)
    
    # Run the workflow
    run_workflow(workflow_name, workflow_args)
    
    
if __name__ == '__main__':
    main()
    
    