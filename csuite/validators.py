#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import tempfile
import argparse
from pathlib import Path


LOG = logging.getLogger(__name__)


def validate_main_args(args: argparse.Namespace) -> dict:
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
    
    return vars(args)


def validate_output_args(args: argparse.Namespace) -> dict:
    # First validate main argument values
    parsed_args = validate_main_args(args)
        
    # Session file should exist
    if not parsed_args['session'].is_file():
        raise FileNotFoundError("Session file not found!")
        
    return parsed_args

