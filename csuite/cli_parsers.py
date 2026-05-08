#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
import logging
from pathlib import Path
from importlib.metadata import version


__version__ = version("csuite")


LOG = logging.getLogger(__name__)


def register_local_structure_derep_subparser(subparsers):
    parser = subparsers.add_parser('local_structure_derep', add_help = False, help = "structure-based search with dereplication")
    
    args_general = parser.add_argument_group('General')
    args_general.add_argument('--cores', dest = 'CFS_lCCL_CFSCDS$cores', metavar = 'cores',
                              default = 1, type = int, 
                              help = "Number of cores available to use (default: 1).")    
    args_general.add_argument('-f', '--force', dest = 'MAIN$force',
                              default = False, action = 'store_true', help = "Force overwriting output (default: False).")
    args_general.add_argument('-vv', '--verbosity', dest = 'MAIN$verbosity', metavar = 'verbosity',
                              default = 3, type = int, choices = [0,1,2,3,4], help = "Console verbosity level (default: 3 (info)).")
    args_general.add_argument('-np', '--no-progress', dest = "CFS_lCCL_CFSCDS$no_progress",
                              default = False, action = 'store_true', help = "Hide most progress bars (default: False).")
    args_general.add_argument('-h', '--help', action = 'help', help = "Show this help message and exit")
    
    args_io = parser.add_argument_group('File inputs and outputs')
    args_io.add_argument('-q', '--query', dest = 'CFS$query_folder', metavar = 'query_folder',
                         required = True, type = Path, help = "Path of the folder containing the query proteins.")
    args_io.add_argument('-o', '--output', dest = 'MAIN$output', metavar = 'output',
                         type = Path, default = Path('.'), help = "Output directory (default: current location)")
    args_io.add_argument('-t', '--temp', dest = "MAIN$temp", metavar = 'temp',
                         type = Path, default = tempfile.gettempdir(), help = "Path to store temporary files (default: your OS's default temporary directory).")
    args_io.add_argument('-g', '--genomes', dest = "lCCL$genome_dir", metavar = 'genome_dir',
                         type = Path, default = '.', 
                         help = "[Only relevant for local searches] Path to local genome folder containing genome files. Accepted formats are FASTA and Genbank [.fasta; .fna; .fa; .gbff; .gbk; .gb]. Files can be gzipped. (default: current working directory)")
    args_io.add_argument('--keep_intermediate', dest = "lCCL$keep_intermediate",
                         default = False, action = "store_true", help = "Keep all intermediate data.")
    
    args_cds_db = parser.add_argument_group('Context database construction options')
    args_cds_db.add_argument('--context-input', dest = 'CFSCDS$input', metavar = 'input',
                             type = Path, default = Path('.'), help = "Path to folder holding the input files or NCBI package (default: current directory)")
    args_cds_db.add_argument('--context-parsing-mode', dest = 'CFSCDS$mode', metavar = 'mode',
                             type = str, required = True, choices = ['ncbi-gff', 'ncbi-package', 'bakta-gff', 'tsv'],
                             help = 'File parsing mode (choices: ncbi-gff, ncbi-package, bakta-gff, tsv).')
    
    args_search = parser.add_argument_group('General search options')
    args_search.add_argument('--search-mode', dest = 'CFS$mode', metavar = 'mode', default = 'local',
                             type = str, choices = ['local', 'local_clustered'], help = "Search mode (default: local)")
    args_search.add_argument('--max-eval', dest = "CFS$max_eval", metavar = 'max_eval',
                             type = float, default = 1e-9, help = "Maximum e-value to include a FoldSeek hit (default: 1e-9).")
    args_search.add_argument('--min-score', dest = "CFS$min_score", metavar = 'min_score',
                             type = float, default = 250, help = "Minimum FoldSeek bitscore to include a hit (default: 250).")
    args_search.add_argument('--min-seqid', dest = "CFS$min_seqid", metavar = 'min_seqid',
                             type = float, default = 0, help = "Minimum sequence identity to include a hit (in percentages) (default: 0).")
    args_search.add_argument('--min-qcov', dest = "CFS$min_qcov", metavar = "min_qcov",
                             type = float, default = 50, help = "Minimum query coverage to include a hit (in percentages) (default: 50).")
    args_search.add_argument('--min-tcov', dest = "CFS$min_tcov", metavar = 'min_tcov',
                             type = float, default = 50, help = "Minimum target coverage to include a hit (in percentages) (default: 50).")
    args_search.add_argument('--max-gap', dest = "CFS$max_gap", metavar = 'max_gap',
                             type = int, default = 5000, help = "Maximum intergenic gap within a cluster (in bp) (default: 5000).")
    args_search.add_argument('--max-length', dest = "CFS$max_length", metavar = "max_length",
                             type = int, default = 1e5, help = "Maximum genomic length of a cluster (in bp) (default: 1e5).")
    args_search.add_argument('--min-hits', dest = "CFS$min_hits", metavar = "min_hits",
                             type = int, default = 2, help = "Minimum number of members in a cluster (default: 2).")
    args_search.add_argument('--min-cov-qrs', dest = "CFS$min_cov_qrs", metavar = "min_cov_qrs",
                             type = int, default = 2, help = "Minimum different queries covered by a cluster (default: 2).")
    args_search.add_argument('--require', dest = "CFS$require", metavar = 'require',
                             type = str, default = '', nargs = '*', help = "Queries that have to present in a cluster (use filenames without extensions).")
    
    args_local = parser.add_argument_group('Local-specific search options')
    args_local.add_argument('-ldb', '--local-db', dest = 'CFS$local_db_path', metavar = 'local_db_path',
                            type = Path, default = Path('local_db/local_db'), help = "Path to your local FoldSeek DB (format: <path-to-containing-folder>/<DB-prefix>) (default: local_db/local_db).")
    
    args_local_clustered = parser.add_argument_group('Local-clustered-specific search options')
    args_local_clustered.add_argument('-scl', '--seq-clusters', dest = "CFS$seq_clusters", metavar = 'seq_clusters',
                                      type = Path, default = Path('cluster_clustered.tsv'),
                                      help = "Path to MMseqs2 clustering table TSV file (default: cluster_clustered.tsv).")
    
    args_dereplication = parser.add_argument_group('Dereplication options')
    args_dereplication.add_argument('--method', dest = 'lCCL$method', metavar = 'method',
                                    default = "genomes", choices = ['genomes', 'regions'], type = str, 
                                    help = "Dereplication method: full genome-based ('genomes') or genomic neighbourhood-based ('regions') (default: genomes)")
    args_dereplication.add_argument('-i', '--identity', dest = 'lCCL$identity', metavar = 'identity',
                                    default = 99.0, type = float, help = "Identity dereplication cutoff (default: 99.0)")
    args_dereplication.add_argument('-c', '--coverage', dest = 'lCCL$coverage', metavar = 'coverage',
                                    default = 80.0, type = float, help = "Coverage dereplication cutoff (default: 80.0)")
    
    args_region_dereplication = parser.add_argument_group('Region-based-specific dereplication options')
    args_region_dereplication.add_argument('-m', '--margin', dest = 'lCCL$margin', metavar = 'margin',
                                           default = 0, type = int, help = "Sequence margin at both sides of the cluster in bp. Required in case of region-based dereplication. (default: 0)")
    
    return None


def register_sequence_derep_subparser(subparsers):
    parser = subparsers.add_parser('sequence_derep', add_help = False, help = "sequence-based search with dereplication")
    
    parser.add_argument('--attemmpt', choices = ['a','b'])
    
    return None

