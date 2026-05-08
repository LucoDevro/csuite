#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging

from csuite.validators import validate_main_args as main_arg_validator
from cfoldseeker.main import parse_and_validate_arguments as cfs_arg_validator
from cfoldseeker.build_cds_db import parse_and_validate_arguments as cfscds_arg_validator
from cagecleaner.validators import parse_and_validate_arguments as ccl_validator

from csuite.defaults import (cfoldseekerDefaultConfiguration,
                             cfoldseekerCDSDefaultConfiguration,
                             CAGEcleanerDefaultConfiguration,
                             mainDefaultConfiguration)

LOG = logging.getLogger(__name__)


WORKFLOW_TOOLS = {'remote_structure': ['MAIN', 'CFS'],
                  'local_structure': ['MAIN', 'CFSCDS', 'CFS'],
                  'remote_structure_derep': ['MAIN', 'CFS', 'rCCL'],
                  'local_structure_derep': ['MAIN', 'CFSCDS', 'CFS', 'lCCL'],
                  'remote_sequence': ['MAIN', 'CBL'],
                  'local_sequence': ['MAIN', 'CBLDB', 'CBL'],
                  'remote_sequence_derep': ['MAIN', 'CBL', 'rCCL'],
                  'local_sequence_derep': ['MAIN', 'CBLDB', 'CBL', 'lCCL'],
                  'derep': ['MAIN', 'CCL'],
                  }

TOOL_DEFAULT_CONFS = {'MAIN': mainDefaultConfiguration(),
                      'CFS': cfoldseekerDefaultConfiguration(),
                      'CFSCDS': cfoldseekerCDSDefaultConfiguration(),
                      'lCCL': CAGEcleanerDefaultConfiguration(),
                      'rCCL': CAGEcleanerDefaultConfiguration(),
                      'CCL': CAGEcleanerDefaultConfiguration()}

TOOL_ARG_VALIDATORS = {'MAIN': main_arg_validator,
                       'CFS': lambda x: cfs_arg_validator(x, skip_csuite_IO_checks = True),
                       'CFSCDS': cfscds_arg_validator,
                       'CCL': ccl_validator,
                       'lCCL': lambda x: ccl_validator(x, bypass_source = 'local'),
                       'rCCL': lambda x: ccl_validator(x, bypass_source = 'remote')}


def categorise_args(args: argparse.Namespace) -> dict[str:argparse.Namespace]:
    all_args = vars(args)
    selected_tools = WORKFLOW_TOOLS[all_args['command']]
    categorised_args = {}
    for tool in selected_tools:
        tool_args = {k.split('$')[1] : v for k,v in all_args.items() if tool in k.split('$')[0].split('_')}
        default_args = TOOL_DEFAULT_CONFS[tool]
        
        tool_args_with_defaults = vars(default_args)
        for arg_key, arg_val in tool_args.items():
            tool_args_with_defaults[arg_key] = arg_val
        
        categorised_args[tool] = argparse.Namespace(**tool_args_with_defaults)
        
    return categorised_args


def parse_and_validate_args(categorised_args: dict[str:argparse.Namespace]) -> dict:
    selected_validators = {tool: TOOL_ARG_VALIDATORS[tool] for tool in categorised_args.keys()}
    parsed_categorised_args = {}
    for tool, validator in selected_validators.items():
        parsed_categorised_args[tool] = validator(categorised_args[tool])
        
    return parsed_categorised_args


