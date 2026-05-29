#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
import logging
from pathlib import Path


LOG = logging.getLogger(__name__)


class cfoldseekerDefaultConfiguration():
    """
    Data class for the default argument values of cfoldseeker.
    """
    def __init__(self):
        self.mode = 'remote'
        self.cores = 1
        self.force = False,
        self.verbosity = 3
        self.no_progress = False
        self.output = Path('.')
        self.output_tables = True
        self.output_session = True
        self.output_summary = True
        self.output_binary = True
        self.output_plot = True
        self.output_clinker = True
        self.output_foldseek = True
        self.max_eval = 1e-9
        self.min_score = float(250)
        self.min_seqid = float(0)
        self.min_qcov = float(50)
        self.min_tcov = float(50)
        self.max_gap = 5000
        self.max_length = 1e5
        self.min_hits = 2
        self.min_cov_qrs = 2
        self.require = ''
        self.all_layouts = False
        self.db = ['afdb50']
        self.taxfilters = ''
        self.mapping_table_path = Path('uniprot_kegg_genpept.gz')
        self.max_workers = 2
        self.local_db_path = Path('local_db/local_db')
        self.cds_db_path = Path('local_cds_db.gz')
        self.seq_clusters = Path('cluster_clustered.tsv')
        

class cfoldseekerCDSDefaultConfiguration():
    """
    Data class for the default argument values of cfoldseeker-cds.
    """
    def __init__(self):
        self.input = Path('.')
        self.output = Path('local_db')
        self.gzip = True
        self.use_taxa = False
        self.cores = 1
        self.force = False
        self.no_progress = False
        

class CAGEcleanerDefaultConfiguration():
    """
    Data class for the default argument values of CAGEcleaner.
    """
    def __init__(self):
        self.cores = 1
        self.force = False
        self.verbosity = 3
        self.no_progress = False,
        self.genome_dir = Path('.')
        self.output = Path('.')
        self.keep_downloads = False
        self.keep_dereplication = False
        self.keep_intermediate = False
        self.bypass_scaffolds = ''
        self.bypass_organisms = ''
        self.excluded_scaffolds = ''
        self.excluded_organisms = ''
        self.download_workers = 2
        self.download_batch = 300
        self.method = 'genomes'
        self.identity = 99.0
        self.coverage = 80.0
        self.low_mem = False
        self.margin = 0
        self.strict_regions = False
        self.no_recovery_by_content = False
        self.no_recovery_by_score = False
        self.zscore_outlier_threshold = 2.0
        self.minimal_score_difference = 0.1
        
        
class mainDefaultConfiguration():
    """
    Data class for the default argument values of the csuite main entry point.
    """
    def __init__(self):
        self.output = Path('.')
        self.temp = Path(tempfile.gettempdir())
    

class reportDefaultConfiguration():
    """
    Data class for the default argument values of the report generation module.
    """
    def __init__(self):
        self.force = False
        self.temp = Path(tempfile.gettempdir())
        self.verbosity = 3
        self.output = Path('.')
        self.output_summary = True
        self.output_binary = True
        self.output_plot = True
        self.output_clinker = True
        
        
class cblasterSearchDefaultConfiguration():
    """
    Data class for the default argument values of cblaster-search.
    """
    def __init__(self):
        self.query_file = None
        self.query_ids = None
        self.query_profiles = None
        self.mode = None
        self.databases = None
        self.database_pfam = None
        self.gap = 5000
        self.unique = 2
        self.min_hits = 2
        self.min_identity = float(30)
        self.min_coverage = float(50)
        self.max_evalue = 1e-3
        self.percentage = None
        self.entrez_query = None
        self.output = None
        self.output_hide_headers = False
        self.output_delimiter = None
        self.output_decimals = 4
        self.output_sort_clusters = False
        self.binary = None
        self.binary_hide_headers = False
        self.binary_delimiter = '\t'
        self.binary_key = len
        self.binary_attr = "identity"
        self.binary_decimals = 4
        self.rid = None
        self.require = None
        self.session_file = [Path('session.json')]
        self.indent = None
        self.plot = False
        self.max_plot_clusters = 50
        self.recompute = False
        self.blast_file = None
        self.ipg_file = None
        self.hitlist_size = 2000
        self.cpus = 1
        self.intermediate_genes = False
        self.intermediate_gene_distance = 5000
        self.intermediate_max_clusters = 0
        self.testing = False
        self.dmnd_sensitivity = 'fast'
        

class cblasterMakedbDefaultConfiguration():
    """
    Data class for the default argument values of cblaster-makedb.
    """
    def __init__(self):
        self.paths = []
        self.database = 'local_db'
        self.force = False
        self.cpus = None
        self.batch = 100
        self.compress = False
        
        
class extractDefaultConfiguration():
    """
    Data class for the default argument values of cluster extraction workflows.
    """
    def __init__(self):
        self.prefix = "",
        self.cluster_numbers = None,
        self.score_threshold = None,
        self.organisms = None,
        self.scaffolds = None,
        self.max_clusters = None
        
