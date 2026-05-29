#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging

from csuite.validators import (validate_main_args,
                               validate_report_args,
                               validate_cblaster_search_args,
                               validate_cblaster_makedb_args,
                               validate_remote_extract_args,
                               validate_local_extract_args,
                               )
from cfoldseeker.main import parse_and_validate_arguments as cfs_arg_validator
from cfoldseeker.build_cds_db import parse_and_validate_arguments as cfscds_arg_validator
from cagecleaner.validators import parse_and_validate_arguments as ccl_arg_validator

from csuite.defaults import (cfoldseekerDefaultConfiguration,
                             cfoldseekerCDSDefaultConfiguration,
                             CAGEcleanerDefaultConfiguration,
                             mainDefaultConfiguration,
                             reportDefaultConfiguration,
                             cblasterSearchDefaultConfiguration,
                             cblasterMakedbDefaultConfiguration,
                             extractDefaultConfiguration,
                             )


LOG = logging.getLogger(__name__)

# List which modules/tools are part of which workflow
WORKFLOW_TOOLS = {'remote_struc': ['MAIN', 'CFS'],
                  'local_struc': ['MAIN', 'CFSCDS', 'CFS'],
                  'remote_struc_derep': ['MAIN', 'CFS', 'rCCL'],
                  'local_struc_derep': ['MAIN', 'CFSCDS', 'CFS', 'lCCL'],
                  'remote_seq': ['MAIN', 'CBL'],
                  'local_seq': ['MAIN', 'CBLDB', 'CBL'],
                  'remote_seq_derep': ['MAIN', 'CBL', 'rCCL'],
                  'local_seq_derep': ['MAIN', 'CBLDB', 'CBL', 'lCCL'],
                  'derep': ['MAIN', 'CCL'],
                  'report': ['MAIN', 'OUT'],
                  'remote_extract': ['MAIN', 'rEXT'],
                  'local_extract': ['MAIN', 'lEXT']
                  }

# Define the default argument values for each tool
TOOL_DEFAULT_CONFS = {'MAIN': mainDefaultConfiguration(),
                      'CFS': cfoldseekerDefaultConfiguration(),
                      'CFSCDS': cfoldseekerCDSDefaultConfiguration(),
                      'lCCL': CAGEcleanerDefaultConfiguration(),
                      'rCCL': CAGEcleanerDefaultConfiguration(),
                      'CCL': CAGEcleanerDefaultConfiguration(),
                      'OUT': reportDefaultConfiguration(),
                      'CBL': cblasterSearchDefaultConfiguration(),
                      'CBLDB': cblasterMakedbDefaultConfiguration(),
                      'rEXT': extractDefaultConfiguration(),
                      'lEXT': extractDefaultConfiguration(),
                      }

# Define the validator function for each tool
TOOL_ARG_VALIDATORS = {'MAIN': validate_main_args,
                       'CFS': lambda x: cfs_arg_validator(x, skip_context_table_check = True),
                       'CFSCDS': cfscds_arg_validator,
                       'CCL': ccl_arg_validator,
                       'lCCL': lambda x: ccl_arg_validator(x, bypass_source = 'local'),
                       'rCCL': lambda x: ccl_arg_validator(x, bypass_source = 'remote'),
                       'OUT': validate_report_args,
                       'CBL': validate_cblaster_search_args,
                       'CBLDB': validate_cblaster_makedb_args,
                       'rEXT': validate_remote_extract_args,
                       'lEXT': validate_local_extract_args,
                       }


def categorise_args(args: argparse.Namespace) -> dict[str:argparse.Namespace]:
    """
    Categorise the argument namespace by workflow.
    
    The arguments collected through the CLI are grouped by the tool that requires them, as indicated through the CLI
    argument labels. Missing argument values are imputed from the default tool configurations.
    
    The argument labels are prefixed by the codename of the tool that requires them.
    For example, an argument `par1` required by tools `tool1` and `tool2` will be encoded as `tool1_tool2$par1`.
    
    Args:
        args (argparse.Namespace): Unparsed CLI argument namespace
        
    Returns:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow, supplemented with default argument values.
    
    Note:
        Categorising arguments is facilitated by toolname prefixes in the argument names (see CLI subparsers.)
    """
    # Temporary parsing of the argument values
    all_args = vars(args)
    
    # Determine selected tools/modules
    selected_tools = WORKFLOW_TOOLS[all_args['command']]
    
    # Categorise arguments by tool
    categorised_args = {}
    for tool in selected_tools:
        # Extract the arguments relevant for this tool using the prefixed argument labels
        tool_args = {k.split('$')[1] : v # Which argument-value pair?
                     for k,v in all_args.items() 
                     if tool in k.split('$')[0].split('_') # Is it required by this tool?
                     }
        
        # Parse default argument values for this tool
        default_args = TOOL_DEFAULT_CONFS[tool]
        tool_args_with_defaults = vars(default_args)
        
        # Add or adjust freshly parsed arguments to the default configuration to end up with a fully populated namespace
        for arg_key, arg_val in tool_args.items():
            tool_args_with_defaults[arg_key] = arg_val
        
        # Define the new namespace for this tool
        categorised_args[tool] = argparse.Namespace(**tool_args_with_defaults)
        
    return categorised_args


def parse_and_validate_args(categorised_args: dict[str:argparse.Namespace]) -> dict:
    """
    Parse and validate the argument namespace for each tool.
    
    Parses the arguments for each tool, and validates them using their associated validator functions.
    
    Args:
        categorised_args (dict[argparse.Namespace]): dictionary of unparsed argument namespaces per tool
            involved in the workflow.
            
    Returns:
        parsed_categorised_args (dict): dictionary of dictionaries of argument name-value pairs, 
            grouped by tool involved in a workflow.
    """
    # Determine which validator functions will be needed for each tool
    selected_validators = {tool: TOOL_ARG_VALIDATORS[tool] for tool in categorised_args.keys()}
    
    # Parse and validate each tool's argument namespace using the selected validator
    parsed_categorised_args = {}
    for tool, validator in selected_validators.items():
        parsed_categorised_args[tool] = validator(categorised_args[tool])
        
    return parsed_categorised_args

