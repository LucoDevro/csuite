#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys

from csuite.cli_parsers import register_sequence_derep_subparser, register_local_structure_derep_subparser
from csuite.argument_parsers import categorise_args
from csuite.workflows import setup_workflow, run_workflow


__version__ = "0.0.0"


LOG = logging.getLogger(__name__)


def create_main_parser():
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
    
    # sequence
    # parser_sequence = subparsers.add_parser('sequence', help = "sequence-based search")
    
    # sequence with dereplication
    # parser_sequence_derep = subparsers.add_parser('sequence_derep', help = "sequence-based search with dereplication")
    register_sequence_derep_subparser(subparsers)
    
    # structure
    # parser_structure = subparsers.add_parser('structure', help = "structure-based search")
    
    # structure with dereplication
    # parser_structure_derep = subparsers.add_parser('structure_derep', help = "structure-based search with dereplication")
    register_local_structure_derep_subparser(subparsers)
    
    # merge sessions
    # parser_merge = subparsers.add_parser('merge', help = 'merge existing sessions')
    
    # dereplicate only
    # parser_derep = subparsers.add_parser('dereplicate', help = 'dereplicate existing search')
    
    # generate output from a session
    # parser_output = subparsers.add_parser('output', help = 'generate a supported output for an existing search')
    
    
    return parser


def setup_logging(verbosity: int) -> None:
    """
    Set up the root logger.
    
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
        handlers = [logging.StreamHandler(sys.stdout)]
        )
    
    return None


def main():
    # Parse args
    parser = create_main_parser()
    args = parser.parse_args()
    workflow_name = args.command
    
    # Categorise them by tool
    categorised_args = categorise_args(args)
    
    # Set up logging
    setup_logging(categorised_args['MAIN'].verbosity)
    
    # Set up the workflow by setting the right I/O arguments
    # Validate arguments on-the-fly, catching and ignoring non-existing 
    # intermediate files for now (will be taken care of by the workflow)
    workflow_args = setup_workflow(workflow_name, categorised_args)
    
    # Run the workflow
    run_workflow(workflow_name, workflow_args)
    
    
if __name__ == '__main__':
    main()
    
    