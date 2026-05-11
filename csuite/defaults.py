#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
import logging
from pathlib import Path


LOG = logging.getLogger(__name__)


class cfoldseekerDefaultConfiguration():
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
    def __init__(self):
        self.input = Path('.')
        self.output = Path('local_db')
        self.gzip = True
        self.use_taxa = False
        self.cores = 1
        self.force = False
        self.no_progress = False
        

class CAGEcleanerDefaultConfiguration():
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
    def __init__(self):
        self.output = Path('.')
        self.temp = Path(tempfile.gettempdir())
    

class outputDefaultConfiguration():
    def __init__(self):
        self.force = False
        self.verbosity = 3
        self.output = Path('.')
        self.output_summary = True
        self.output_binary = True
        self.output_plot = True
        self.output_clinker = True
        
        
