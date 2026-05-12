#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
import logging
from pathlib import Path
from importlib.metadata import version

from cblaster.parsers import NCBI_DATABASES


__version__ = version("csuite")


LOG = logging.getLogger(__name__)


def register_local_struc_derep_subparser(subparsers):
    parser = subparsers.add_parser('local_struc_derep', add_help = False,
                                   help = "local structure-based search with dereplication")
    
    args_general = parser.add_argument_group('General')
    args_general.add_argument('--cores', dest = 'MAIN$cores', metavar = 'cores',
                              default = 1, type = int, 
                              help = "Number of cores available to use (default: 1).")    
    args_general.add_argument('-f', '--force', dest = 'MAIN$force',
                              default = False, action = 'store_true', help = "Force overwriting output (default: False).")
    args_general.add_argument('-vv', '--verbosity', dest = 'MAIN$verbosity', metavar = 'verbosity',
                              default = 3, type = int, choices = [0,1,2,3,4], help = "Console verbosity level (default: 3 (info)).")
    args_general.add_argument('-np', '--no-progress', dest = "MAIN$no_progress",
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
    args_io.add_argument('--keep_temp_derep', dest = "lCCL$keep_intermediate",
                         default = False, action = "store_true", help = "Keep all temporary dereplication data.")
    
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


def register_local_struc_subparser(subparsers):
    parser = subparsers.add_parser('local_struc', add_help = False,
                                   help = "local structure-based search")
    
    args_general = parser.add_argument_group('General')
    args_general.add_argument('--cores', dest = 'MAIN$cores', metavar = 'cores',
                              default = 1, type = int, 
                              help = "Number of cores available to use (default: 1).")    
    args_general.add_argument('-f', '--force', dest = 'MAIN$force',
                              default = False, action = 'store_true', help = "Force overwriting output (default: False).")
    args_general.add_argument('-vv', '--verbosity', dest = 'MAIN$verbosity', metavar = 'verbosity',
                              default = 3, type = int, choices = [0,1,2,3,4], help = "Console verbosity level (default: 3 (info)).")
    args_general.add_argument('-np', '--no-progress', dest = "MAIN$no_progress",
                              default = False, action = 'store_true', help = "Hide most progress bars (default: False).")
    args_general.add_argument('-h', '--help', action = 'help', help = "Show this help message and exit")
    
    args_io = parser.add_argument_group('File inputs and outputs')
    args_io.add_argument('-q', '--query', dest = 'CFS$query_folder', metavar = 'query_folder',
                         required = True, type = Path, help = "Path of the folder containing the query proteins.")
    args_io.add_argument('-o', '--output', dest = 'MAIN$output', metavar = 'output',
                         type = Path, default = Path('.'), help = "Output directory (default: current location)")
    args_io.add_argument('-t', '--temp', dest = "MAIN$temp", metavar = 'temp',
                         type = Path, default = tempfile.gettempdir(), help = "Path to store temporary files (default: your OS's default temporary directory).")
    
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
    
    return None


def register_remote_struc_derep_subparser(subparsers):
    parser = subparsers.add_parser('remote_struc_derep', add_help = False,
                                   help = "remote structure-based search with dereplication")
    
    args_general = parser.add_argument_group('General')
    args_general.add_argument('--cores', dest = 'MAIN$cores', metavar = 'cores',
                              default = 1, type = int, 
                              help = "Number of cores available to use (default: 1).")    
    args_general.add_argument('-f', '--force', dest = 'MAIN$force',
                              default = False, action = 'store_true', help = "Force overwriting output (default: False).")
    args_general.add_argument('-vv', '--verbosity', dest = 'MAIN$verbosity', metavar = 'verbosity',
                              default = 3, type = int, choices = [0,1,2,3,4], help = "Console verbosity level (default: 3 (info)).")
    args_general.add_argument('-np', '--no-progress', dest = "MAIN$no_progress",
                              default = False, action = 'store_true', help = "Hide most progress bars (default: False).")
    args_general.add_argument('-h', '--help', action = 'help', help = "Show this help message and exit")
    
    args_io = parser.add_argument_group('File inputs and outputs')
    args_io.add_argument('-q', '--query', dest = 'CFS$query_folder', metavar = 'query_folder',
                         required = True, type = Path, help = "Path of the folder containing the query proteins.")
    args_io.add_argument('-o', '--output', dest = 'MAIN$output', metavar = 'output',
                         type = Path, default = Path('.'), help = "Output directory (default: current location)")
    args_io.add_argument('-t', '--temp', dest = "MAIN$temp", metavar = 'temp',
                         type = Path, default = tempfile.gettempdir(), help = "Path to store temporary files (default: your OS's default temporary directory).")
    args_io.add_argument('--keep_temp_derep', dest = "rCCL$keep_intermediate",
                         default = False, action = "store_true", help = "Keep all temporary dereplication data.")
    
    args_search = parser.add_argument_group('General search options')
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
    
    args_remote = parser.add_argument_group("Remote-specific search options")
    args_remote.add_argument('-rdb', '--remote-db', dest = 'CFS$db', metavar = "db",
                             type = str, default = ['afdb50'], nargs = '+', choices = ['afdb-proteome', 'afdb-swissprot', 'afdb50'], 
                             help = "Remote target database (default: afdb50) (choices: afdb-proteome, afdb-swissprot, afdb50)")
    args_remote.add_argument('-tf', '--taxon-filter', dest = 'CFS$taxfilters', metavar = "taxfilters",
                             type = str, default = '', nargs = '*',
                             help = "Taxon ID(s) to filter the FoldSeek results table.")
    args_remote.add_argument('-uma', '--uniprot-mapping', dest = 'CFS$mapping_table_path', metavar = "mapping_table_path",
                             type = Path, default = Path('uniprot_kegg_genpept.gz'),
                             help = "Path to the UniProt AFDB ID mapping table (default: uniprot_kegg_genpept.gz)")
    args_remote.add_argument('-w', '--max-workers', dest = "CFS$max_workers", metavar = "max_workers",
                             type = int, default = 2,
                             help = "Maximum number of workers to query the remote servers (FoldSeek, KEGG, ENA) (default: 2)")
    
    args_dereplication = parser.add_argument_group('Dereplication options')
    args_dereplication.add_argument('--method', dest = 'rCCL$method', metavar = 'method',
                                    default = "genomes", choices = ['genomes', 'regions'], type = str, 
                                    help = "Dereplication method: full genome-based ('genomes') or genomic neighbourhood-based ('regions') (default: genomes)")
    args_dereplication.add_argument('-i', '--identity', dest = 'rCCL$identity', metavar = 'identity',
                                    default = 99.0, type = float, help = "Identity dereplication cutoff (default: 99.0)")
    args_dereplication.add_argument('-c', '--coverage', dest = 'rCCL$coverage', metavar = 'coverage',
                                    default = 80.0, type = float, help = "Coverage dereplication cutoff (default: 80.0)")
    
    args_region_dereplication = parser.add_argument_group('Region-based-specific dereplication options')
    args_region_dereplication.add_argument('-m', '--margin', dest = 'rCCL$margin', metavar = 'margin',
                                           default = 0, type = int, help = "Sequence margin at both sides of the cluster in bp. Required in case of region-based dereplication. (default: 0)")
    
    return None


def register_remote_struc_subparser(subparsers):
    parser = subparsers.add_parser('remote_struc', add_help = False,
                                   help = "remote structure-based search")
    
    args_general = parser.add_argument_group('General')
    args_general.add_argument('--cores', dest = 'MAIN$cores', metavar = 'cores',
                              default = 1, type = int, 
                              help = "Number of cores available to use (default: 1).")    
    args_general.add_argument('-f', '--force', dest = 'MAIN$force',
                              default = False, action = 'store_true', help = "Force overwriting output (default: False).")
    args_general.add_argument('-vv', '--verbosity', dest = 'MAIN$verbosity', metavar = 'verbosity',
                              default = 3, type = int, choices = [0,1,2,3,4], help = "Console verbosity level (default: 3 (info)).")
    args_general.add_argument('-np', '--no-progress', dest = "MAIN$no_progress",
                              default = False, action = 'store_true', help = "Hide most progress bars (default: False).")
    args_general.add_argument('-h', '--help', action = 'help', help = "Show this help message and exit")
    
    args_io = parser.add_argument_group('File inputs and outputs')
    args_io.add_argument('-q', '--query', dest = 'CFS$query_folder', metavar = 'query_folder',
                         required = True, type = Path, help = "Path of the folder containing the query proteins.")
    args_io.add_argument('-o', '--output', dest = 'MAIN$output', metavar = 'output',
                         type = Path, default = Path('.'), help = "Output directory (default: current location)")
    args_io.add_argument('-t', '--temp', dest = "MAIN$temp", metavar = 'temp',
                         type = Path, default = tempfile.gettempdir(), help = "Path to store temporary files (default: your OS's default temporary directory).")
    
    args_search = parser.add_argument_group('General search options')
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
    
    args_remote = parser.add_argument_group("Remote-specific search options")
    args_remote.add_argument('-rdb', '--remote-db', dest = 'CFS$db', metavar = "db",
                             type = str, default = ['afdb50'], nargs = '+', choices = ['afdb-proteome', 'afdb-swissprot', 'afdb50'], 
                             help = "Remote target database (default: afdb50) (choices: afdb-proteome, afdb-swissprot, afdb50)")
    args_remote.add_argument('-tf', '--taxon-filter', dest = 'CFS$taxfilters', metavar = "taxfilters",
                             type = str, default = '', nargs = '*',
                             help = "Taxon ID(s) to filter the FoldSeek results table.")
    args_remote.add_argument('-uma', '--uniprot-mapping', dest = 'CFS$mapping_table_path', metavar = "mapping_table_path",
                             type = Path, default = Path('uniprot_kegg_genpept.gz'),
                             help = "Path to the UniProt AFDB ID mapping table (default: uniprot_kegg_genpept.gz)")
    args_remote.add_argument('-w', '--max-workers', dest = "CFS$max_workers", metavar = "max_workers",
                             type = int, default = 2,
                             help = "Maximum number of workers to query the remote servers (FoldSeek, KEGG, ENA) (default: 2)")
    
    return None


def register_derep_subparser(subparsers):
    parser = subparsers.add_parser('derep', add_help = False,
                                   help = "dereplication")
    
    args_general = parser.add_argument_group('General')
    args_general.add_argument('--cores', dest = 'MAIN$cores', metavar = 'cores',
                              default = 1, type = int, 
                              help = "Number of cores available to use (default: 1).")    
    args_general.add_argument('-f', '--force', dest = 'MAIN$force',
                              default = False, action = 'store_true', help = "Force overwriting output (default: False).")
    args_general.add_argument('-vv', '--verbosity', dest = 'MAIN$verbosity', metavar = 'verbosity',
                              default = 3, type = int, choices = [0,1,2,3,4], help = "Console verbosity level (default: 3 (info)).")
    args_general.add_argument('-np', '--no-progress', dest = "MAIN$no_progress",
                              default = False, action = 'store_true', help = "Hide most progress bars (default: False).")
    args_general.add_argument('-h', '--help', action = 'help', help = "Show this help message and exit")
    
    args_io = parser.add_argument_group('File inputs and outputs')
    args_io.add_argument('-s', '--session', dest = "CCL$session", metavar = "session",
                         type = Path, required = True,
                         help = "Path to cblaster session (either obtained from a search run or from cagecleaner-generate-session).")
    args_io.add_argument('-o', '--output', dest = 'MAIN$output', metavar = 'output',
                         type = Path, default = Path('.'), help = "Output directory (default: current location)")
    args_io.add_argument('-g', '--genomes', dest = "CCL$genome_dir", metavar = 'genome_dir',
                         type = Path, default = '.', 
                         help = "[Only relevant for local searches] Path to local genome folder containing genome files. Accepted formats are FASTA and Genbank [.fasta; .fna; .fa; .gbff; .gbk; .gb]. Files can be gzipped. (default: current working directory)")
    args_io.add_argument('-t', '--temp', dest = "MAIN$temp", metavar = 'temp',
                         type = Path, default = tempfile.gettempdir(), help = "Path to store temporary files (default: your OS's default temporary directory).")
    args_io.add_argument('--keep_temp_derep', dest = "CCL$keep_intermediate",
                         default = False, action = "store_true", help = "Keep all temporary dereplication data.")
    
    args_dereplication = parser.add_argument_group('Dereplication options')
    args_dereplication.add_argument('--method', dest = 'CCL$method', metavar = 'method',
                                    default = "genomes", choices = ['genomes', 'regions'], type = str, 
                                    help = "Dereplication method: full genome-based ('genomes') or genomic neighbourhood-based ('regions') (default: genomes)")
    args_dereplication.add_argument('-i', '--identity', dest = 'CCL$identity', metavar = 'identity',
                                    default = 99.0, type = float, help = "Identity dereplication cutoff (default: 99.0)")
    args_dereplication.add_argument('-c', '--coverage', dest = 'CCL$coverage', metavar = 'coverage',
                                    default = 80.0, type = float, help = "Coverage dereplication cutoff (default: 80.0)")
    
    args_region_dereplication = parser.add_argument_group('Region-based-specific dereplication options')
    args_region_dereplication.add_argument('-m', '--margin', dest = 'CCL$margin', metavar = 'margin',
                                           default = 0, type = int, help = "Sequence margin at both sides of the cluster in bp. Required in case of region-based dereplication. (default: 0)")
    
    return None


def register_output_subparser(subparsers):
    parser = subparsers.add_parser('output', add_help = False,
                                   help = "make plots for an existing session")
    
    args_general = parser.add_argument_group('General')
    args_general.add_argument('-f', '--force', dest = 'MAIN$force',
                              default = False, action = 'store_true', help = "Force overwriting output (default: False).")
    args_general.add_argument('-vv', '--verbosity', dest = 'MAIN$verbosity', metavar = 'verbosity',
                              default = 3, type = int, choices = [0,1,2,3,4], help = "Console verbosity level (default: 3 (info)).")
    args_general.add_argument('-h', '--help', action = 'help', help = "Show this help message and exit")
    
    args_io = parser.add_argument_group('File inputs and outputs')
    args_io.add_argument('-s', '--session', dest = "OUT$session", metavar = "session",
                         type = Path, required = True,
                         help = "Path to cblaster session (either obtained from a search run or from cagecleaner-generate-session).")
    args_io.add_argument('-o', '--output', dest = 'MAIN$output', metavar = 'output',
                         type = Path, default = Path('.'), help = "Output directory (default: current location)")
    args_io.add_argument('-t', '--temp', dest = "MAIN$temp", metavar = 'temp',
                         type = Path, default = tempfile.gettempdir(), help = "Path to store temporary files (default: your OS's default temporary directory).")
    
    args_outputs = parser.add_argument_group('Output types')
    args_outputs.add_argument('--summary', dest = 'OUT$output_summary',
                              default = True, action = 'store_false', help = "Write cblaster summary file (default: True).")
    args_outputs.add_argument('--binary', dest = 'OUT$output_binary',
                              default = True, action = 'store_false', help = "Write cblaster binary file (tab-separated) (default: True).")
    args_outputs.add_argument('--plot', dest = 'OUT$output_plot',
                              default = True, action = 'store_false', help = "Write cblaster clusterplot file (default: True).")
    args_outputs.add_argument('--clinker', dest = 'OUT$output_clinker',
                              default = True, action = 'store_false', help = "Write clinker plot file (default: True).")
    
    return None


def register_remote_seq_subparser(subparsers):
    parser = subparsers.add_parser('remote_seq', add_help = False,
                                   help = "remote sequence-based search")
    
    args_general = parser.add_argument_group('General')
    args_general.add_argument('--cores', dest = 'MAIN$cores', metavar = 'cores', default = 1, type = int, 
                              help = "Number of cores available to use (default: 1).")    
    args_general.add_argument('-f', '--force', dest = 'MAIN$force',
                              default = False, action = 'store_true', help = "Force overwriting output (default: False).")
    args_general.add_argument('-vv', '--verbosity', dest = 'MAIN$verbosity', metavar = 'verbosity',
                              default = 3, type = int, choices = [0,1,2,3,4], help = "Console verbosity level (default: 3 (info)).")
    args_general.add_argument('-h', '--help', action = 'help', help = "Show this help message and exit")
    
    args_io = parser.add_argument_group('File inputs and outputs')
    args_io.add_argument('-q', '--query', dest = 'CBL$query_file', metavar = 'query_file',
                         required = True, type = Path, help = "Path to the query sequence fasta file.")
    args_io.add_argument('-o', '--output', dest = 'MAIN$output', metavar = 'output',
                         type = Path, default = Path('.'), help = "Output directory (default: current location)")
    
    args_search = parser.add_argument_group('Search options')
    args_search.add_argument("-db", "--database", dest = 'CBL$databases', metavar = 'databases', default=["nr"], 
                             nargs="+", type=str, choices = list(NCBI_DATABASES),
                             help="NCBI database to be searched (default: 'nr')")
    args_search.add_argument("-eq", "--entrez_query", dest = 'CBL$entrez_query', metavar = 'entrez_query',
                             help = "An NCBI Entrez search term for pre-search filtering of an NCBI database (e.g. 'Aspergillus'[organism]")
    args_search.add_argument('--max-eval', dest = "CBL$max_evalue", metavar = 'max_eval', type = float, default = 1e-3,
                             help = "Maximum e-value to include a BLAST hit (default: 1e-3).")
    args_search.add_argument('--min-seqid', dest = "CBL$min_identity", metavar = 'min_seqid', type = float, default = 30,
                             help = "Minimum sequence identity to include a hit (in percentages) (default: 30).")
    args_search.add_argument('--min-qcov', dest = "CBL$min_coverage", metavar = 'min_qcov', type = float, default = 50,
                             help = "Minimum query coverage to include a hit (in percentages) (default: 50).")
    args_search.add_argument("--max-gap", dest = 'CBL$gap', metavar = 'max_gap', type = int, default = 5000, 
                             help = "Maximum intergenic gap within a cluster (in bp) (default: 5000).")
    args_search.add_argument("--min-cov-qrs", dest = "CBL$unique", metavar = 'min_cov_qrs', type = int, default = 2,
                             help = "Minimum different queries covered by a cluster (default: 2).")
    args_search.add_argument("--min_hits", dest = "CBL$min_hits", metavar = 'min_hits', type = int, default = 2,
                             help = "Minimum number of members in a cluster (default: 2).")
    args_search.add_argument('--require', dest = "CBL$require", metavar = 'require', type = str, default = '', nargs = '*',
                             help = "Queries that have to present in a cluster (default: None).")
    args_search.add_argument("--percentage", dest = 'CBL$percentage', metavar = 'percentage', type = int, default = 0,
                             help = "Percentage of query genes required to be present in cluster (default: 0).")
    
    return None


def register_local_seq_subparser(subparsers):
    parser = subparsers.add_parser('local_seq', add_help = False,
                                   help = "local sequence-based search")
    
    args_general = parser.add_argument_group('General')
    args_general.add_argument('--cores', dest = 'MAIN$cores', metavar = 'cores', default = 1, type = int, 
                              help = "Number of cores available to use (default: 1).")    
    args_general.add_argument('-f', '--force', dest = 'MAIN$force',
                              default = False, action = 'store_true', help = "Force overwriting output (default: False).")
    args_general.add_argument('-vv', '--verbosity', dest = 'MAIN$verbosity', metavar = 'verbosity',
                              default = 3, type = int, choices = [0,1,2,3,4], help = "Console verbosity level (default: 3 (info)).")
    args_general.add_argument('-h', '--help', action = 'help', help = "Show this help message and exit")
    
    args_io = parser.add_argument_group('File inputs and outputs')
    args_io.add_argument('-q', '--query', dest = 'CBL$query_file', metavar = 'query_file',
                         required = True, type = Path, help = "Path to the query sequence fasta file.")
    args_io.add_argument('-o', '--output', dest = 'MAIN$output', metavar = 'output',
                         type = Path, default = Path('.'), help = "Output directory (default: current location)")
    args_io.add_argument('-g', '--genomes', dest = 'CBLDB$paths', metavar = 'genomes', type = Path, default = Path,
                         help = 'Path to folder containing the local genome files to search in. Should contain Genbank files or pairs of Fasta and GFF files. (default: current location).')
    
    args_search = parser.add_argument_group('Search options')
    args_search.add_argument('--max-eval', dest = "CBL$max_evalue", metavar = 'max_eval', type = float, default = 1e-3,
                             help = "Maximum e-value to include a BLAST hit (default: 1e-3).")
    args_search.add_argument('--min-seqid', dest = "CBL$min_identity", metavar = 'min_seqid', type = float, default = 30,
                             help = "Minimum sequence identity to include a hit (in percentages) (default: 30).")
    args_search.add_argument('--min-qcov', dest = "CBL$min_coverage", metavar = 'min_qcov', type = float, default = 50,
                             help = "Minimum query coverage to include a hit (in percentages) (default: 50).")
    args_search.add_argument("--max-gap", dest = 'CBL$gap', metavar = 'max_gap', type = int, default = 5000, 
                             help = "Maximum intergenic gap within a cluster (in bp) (default: 5000).")
    args_search.add_argument("--min-cov-qrs", dest = "CBL$unique", metavar = 'min_cov_qrs', type = int, default = 2,
                             help = "Minimum different queries covered by a cluster (default: 2).")
    args_search.add_argument("--min_hits", dest = "CBL$min_hits", metavar = 'min_hits', type = int, default = 2,
                             help = "Minimum number of members in a cluster (default: 2).")
    args_search.add_argument('--require', dest = "CBL$require", metavar = 'require', type = str, default = '', nargs = '*',
                             help = "Queries that have to present in a cluster (default: None).")
    args_search.add_argument("--percentage", dest = 'CBL$percentage', metavar = 'percentage', type = int, default = 0,
                             help = "Percentage of query genes required to be present in cluster (default: 0).")
    
    return None


def register_local_seq_derep_subparser(subparsers):
    parser = subparsers.add_parser('local_seq_derep', add_help = False,
                                   help = "local sequence-based search with dereplication")
    
    args_general = parser.add_argument_group('General')
    args_general.add_argument('--cores', dest = 'MAIN$cores', metavar = 'cores', default = 1, type = int, 
                              help = "Number of cores available to use (default: 1).")    
    args_general.add_argument('-f', '--force', dest = 'MAIN$force',
                              default = False, action = 'store_true', help = "Force overwriting output (default: False).")
    args_general.add_argument('-vv', '--verbosity', dest = 'MAIN$verbosity', metavar = 'verbosity',
                              default = 3, type = int, choices = [0,1,2,3,4], help = "Console verbosity level (default: 3 (info)).")
    args_general.add_argument('-np', '--no-progress', dest = "MAIN$no_progress",
                              default = False, action = 'store_true', help = "Hide most progress bars (default: False).")
    args_general.add_argument('-h', '--help', action = 'help', help = "Show this help message and exit")
    
    args_io = parser.add_argument_group('File inputs and outputs')
    args_io.add_argument('-q', '--query', dest = 'CBL$query_file', metavar = 'query_file',
                         required = True, type = Path, help = "Path to the query sequence fasta file.")
    args_io.add_argument('-o', '--output', dest = 'MAIN$output', metavar = 'output',
                         type = Path, default = Path('.'), help = "Output directory (default: current location)")
    args_io.add_argument('-g', '--genomes', dest = 'CBLDB$paths', metavar = 'genomes', type = Path, default = Path,
                         help = 'Path to folder containing the local genome files to search in. Should contain Genbank files or pairs of Fasta and GFF files. (default: current location).')
    args_io.add_argument('-t', '--temp', dest = "MAIN$temp", metavar = 'temp',
                         type = Path, default = tempfile.gettempdir(), help = "Path to store temporary files (default: your OS's default temporary directory).")
    args_io.add_argument('--keep_temp_derep', dest = "lCCL$keep_intermediate",
                         default = False, action = "store_true", help = "Keep all temporary dereplication data.")
    
    args_search = parser.add_argument_group('Search options')
    args_search.add_argument('--max-eval', dest = "CBL$max_evalue", metavar = 'max_eval', type = float, default = 1e-3,
                             help = "Maximum e-value to include a BLAST hit (default: 1e-3).")
    args_search.add_argument('--min-seqid', dest = "CBL$min_identity", metavar = 'min_seqid', type = float, default = 30,
                             help = "Minimum sequence identity to include a hit (in percentages) (default: 30).")
    args_search.add_argument('--min-qcov', dest = "CBL$min_coverage", metavar = 'min_qcov', type = float, default = 50,
                             help = "Minimum query coverage to include a hit (in percentages) (default: 50).")
    args_search.add_argument("--max-gap", dest = 'CBL$gap', metavar = 'max_gap', type = int, default = 5000, 
                             help = "Maximum intergenic gap within a cluster (in bp) (default: 5000).")
    args_search.add_argument("--min-cov-qrs", dest = "CBL$unique", metavar = 'min_cov_qrs', type = int, default = 2,
                             help = "Minimum different queries covered by a cluster (default: 2).")
    args_search.add_argument("--min_hits", dest = "CBL$min_hits", metavar = 'min_hits', type = int, default = 2,
                             help = "Minimum number of members in a cluster (default: 2).")
    args_search.add_argument('--require', dest = "CBL$require", metavar = 'require', type = str, default = '', nargs = '*',
                             help = "Queries that have to present in a cluster (default: None).")
    args_search.add_argument("--percentage", dest = 'CBL$percentage', metavar = 'percentage', type = int, default = 0,
                             help = "Percentage of query genes required to be present in cluster (default: 0).")
    
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


def register_remote_seq_derep_subparser(subparsers):
    parser = subparsers.add_parser('remote_seq_derep', add_help = False,
                                   help = "remote sequence-based search with dereplication")
    
    args_general = parser.add_argument_group('General')
    args_general.add_argument('--cores', dest = 'MAIN$cores', metavar = 'cores', default = 1, type = int, 
                              help = "Number of cores available to use (default: 1).")    
    args_general.add_argument('-f', '--force', dest = 'MAIN$force',
                              default = False, action = 'store_true', help = "Force overwriting output (default: False).")
    args_general.add_argument('-vv', '--verbosity', dest = 'MAIN$verbosity', metavar = 'verbosity',
                              default = 3, type = int, choices = [0,1,2,3,4], help = "Console verbosity level (default: 3 (info)).")
    args_general.add_argument('-np', '--no-progress', dest = "MAIN$no_progress",
                              default = False, action = 'store_true', help = "Hide most progress bars (default: False).")
    args_general.add_argument('-h', '--help', action = 'help', help = "Show this help message and exit")
    
    args_io = parser.add_argument_group('File inputs and outputs')
    args_io.add_argument('-q', '--query', dest = 'CBL$query_file', metavar = 'query_file',
                         required = True, type = Path, help = "Path to the query sequence fasta file.")
    args_io.add_argument('-o', '--output', dest = 'MAIN$output', metavar = 'output',
                         type = Path, default = Path('.'), help = "Output directory (default: current location)")
    args_io.add_argument('-t', '--temp', dest = "MAIN$temp", metavar = 'temp',
                         type = Path, default = tempfile.gettempdir(), help = "Path to store temporary files (default: your OS's default temporary directory).")
    args_io.add_argument('--keep_temp_derep', dest = "rCCL$keep_intermediate",
                         default = False, action = "store_true", help = "Keep all temporary dereplication data.")
    
    args_search = parser.add_argument_group('Search options')
    args_search.add_argument("-db", "--database", dest = 'CBL$databases', metavar = 'databases', default=["nr"], 
                             nargs="+", type=str, choices = list(NCBI_DATABASES),
                             help="NCBI database to be searched (default: 'nr')")
    args_search.add_argument("-eq", "--entrez_query", dest = 'CBL$entrez_query', metavar = 'entrez_query',
                             help = "An NCBI Entrez search term for pre-search filtering of an NCBI database (e.g. 'Aspergillus'[organism]")
    args_search.add_argument('--max-eval', dest = "CBL$max_evalue", metavar = 'max_eval', type = float, default = 1e-3,
                             help = "Maximum e-value to include a BLAST hit (default: 1e-3).")
    args_search.add_argument('--min-seqid', dest = "CBL$min_identity", metavar = 'min_seqid', type = float, default = 30,
                             help = "Minimum sequence identity to include a hit (in percentages) (default: 30).")
    args_search.add_argument('--min-qcov', dest = "CBL$min_coverage", metavar = 'min_qcov', type = float, default = 50,
                             help = "Minimum query coverage to include a hit (in percentages) (default: 50).")
    args_search.add_argument("--max-gap", dest = 'CBL$gap', metavar = 'max_gap', type = int, default = 5000, 
                             help = "Maximum intergenic gap within a cluster (in bp) (default: 5000).")
    args_search.add_argument("--min-cov-qrs", dest = "CBL$unique", metavar = 'min_cov_qrs', type = int, default = 2,
                             help = "Minimum different queries covered by a cluster (default: 2).")
    args_search.add_argument("--min_hits", dest = "CBL$min_hits", metavar = 'min_hits', type = int, default = 2,
                             help = "Minimum number of members in a cluster (default: 2).")
    args_search.add_argument('--require', dest = "CBL$require", metavar = 'require', type = str, default = '', nargs = '*',
                             help = "Queries that have to present in a cluster (default: None).")
    args_search.add_argument("--percentage", dest = 'CBL$percentage', metavar = 'percentage', type = int, default = 0,
                             help = "Percentage of query genes required to be present in cluster (default: 0).")
    
    args_dereplication = parser.add_argument_group('Dereplication options')
    args_dereplication.add_argument('--method', dest = 'rCCL$method', metavar = 'method',
                                    default = "genomes", choices = ['genomes', 'regions'], type = str, 
                                    help = "Dereplication method: full genome-based ('genomes') or genomic neighbourhood-based ('regions') (default: genomes)")
    args_dereplication.add_argument('-i', '--identity', dest = 'rCCL$identity', metavar = 'identity',
                                    default = 99.0, type = float, help = "Identity dereplication cutoff (default: 99.0)")
    args_dereplication.add_argument('-c', '--coverage', dest = 'rCCL$coverage', metavar = 'coverage',
                                    default = 80.0, type = float, help = "Coverage dereplication cutoff (default: 80.0)")
    
    args_region_dereplication = parser.add_argument_group('Region-based-specific dereplication options')
    args_region_dereplication.add_argument('-m', '--margin', dest = 'rCCL$margin', metavar = 'margin',
                                           default = 0, type = int, help = "Sequence margin at both sides of the cluster in bp. Required in case of region-based dereplication. (default: 0)")
    
    return None

