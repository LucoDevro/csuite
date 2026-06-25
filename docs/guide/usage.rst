Getting started
================

A ``csuite`` workflow wraps multiple tools into one streamlined pipeline. We optimised for nicely integrated workflows that start from as many raw inputs as possible (query and target fasta files, query protein structures), but are not too time- or resource-intensive to run in one go.

Remote runs nicely allow for this as much of the heavy lifting has been outsourced to a webserver. However, for local runs, we kept heavy upstream tasks that are not directly related to the search itself out of the pipeline. These should be run separately beforehand.

.. tip::

   For more extensive documentation of all options and outputs, we refer to the documentation of the csuite member tools (`cblaster <https://cblaster.readthedocs.io/en/latest/>`_,  `cfoldseeker <https://cfoldseeker.readthedocs.io/en/latest/>`_,  `CAGEcleaner <https://cagecleaner.readthedocs.io/en/latest/>`_).


Remote searches
---------------

Remote runs are the easiest to get started.

For **structure-based searches** against the AFDB50 database at default settings, run the ``remote_struc`` workflow.

.. code-block:: bash

	csuite remote_struc -q <query-folder> -uma <UniProt-ID-mapping-table>

To **include hit dereplication** at default settings (genome-based at 99% identity and 80% coverage), run the ``remote_struc_derep`` workflow. *Don't forget to download the location of the UniProt ID mapping table!*

.. code-block:: bash

	csuite remote_struc_derep -q <query-folder> -uma <UniProt-ID-mapping-table>

**Sequence-based searches** against the default database (NCBI nr) at default search settings can be done using the ``remote_seq`` workflow.

.. code-block:: bash

	csuite remote_seq -q <query-fasta>

To **include a region-based hit dereplication** with sequence margins of 5 kb, run the ``remote_seq_derep`` workflow with the additional non-default dereplication settings.

.. code-block:: bash

	csuite remote_seq_derep -q <query-fasta> --derep-method regions -m 5000


Local searches
--------------

**Local sequence-based runs** are fully covered starting from your local Genbank genome files. For example, to run a local sequence-based search with default hit dereplication, run the ``local_seq_derep`` workflow. This will construct a cblaster genome database and search your query sequences against it.

.. code-block:: bash

	csuite local_seq_derep -q <query-fasta> -gb <target-genomes>

**Local structure-based searches** may still require some time- and resource-intensive tasks to be done beforehand. These may include generating a target protein structure database from your sequence database using ProstT5, and/or preclustering your target sequence database using MMseqs2.

For example, to run a local structure-based search against a preclustered sequence database, you need to execute a MMseqs2 clustering and then generate protein structures for the sequence cluster representatives using ProstT5 via FoldSeek.

.. tip::

	For a thorough walkthrough of the necessary prior work for local structure-based searches with preclustering, check out the `cfoldseeker tutorial <https://cfoldseeker.readthedocs.io/en/stable/guide/tutorial.html>`_.


.. warning::

	MMseqs2 clustering and ProstT5 protein structure generation are computationally heavy tasks! Consider moving to an HPC environment (with GPUs).

For example, the command sequence for a local structure-based search against a preclustered database of NCBI-sourced proteomes with genome-based hit dereplication at an identity threshold of 96% might look like below.

.. code-block:: bash

	# prior work
	mmseqs easy-linclust <query-folder>/\*.faa clustered tmp
	foldseek createdb clustered_rep_seq.fasta clustered_rep_struc_DB --prostt5-model <path-to-prostt5-weights>

	# search itself
	csuite local_struc_derep \
	-q <query-folder> \
	--context-input <path-to-target-genbanks> \
	--context-parsing-mode <genbank-parsing-mode> \
	--search-mode local_clustered \
	-ldb clustered_rep_struc_DB 
	-scl clustered_cluster.tsv \
	--derep-method genomes \
	-i 96


Report generation
-----------------
For any workflow, run the ``report`` workflow afterwards to get **typical cblaster-like outputs** from the newly generated session file (e.g. binary presence/absence table, summary file, clinker plot...). See the `cblaster docs <https://cblaster.readthedocs.io/en/latest/guide/search_module.html#specifying-output>`_ for more information.

.. code-block:: bash

	csuite report -s <session-file>


Sequence extraction
-------------------
Both sequence extraction workflows facilitate generating Genbank files for each identified cluster, which allows for downstream analyses using other tools.

The remote-mode sequence extractor uses `cblaster extract_clusters` to fetch the sequences remotely from NCBI, and supports both sequence- and structure-based search sessions. The local-mode extractor calls `cfoldseeker-seqs` to do the local sequence fetching for both sequence- and structure-based search sessions.

To extract all cluster Genbank files from a **remote search** session into a folder `clusters`, run

.. code-block:: bash

	csuite remote_extract -s <session-file> -o clusters

For more specifics on the filtering options, have a look at the `cblaster extract_clusters documentation <https://cblaster.readthedocs.io/en/latest/guide/extract_clusters_module.html>`_.

To extract all cluster Genbanks from a **local search** session into a folder `clusters`, add the path to your folder of local genome Genbank files.

.. code-block:: bash

	csuite local_extract -s <session-file> -o clusters -gb <local-genome-genbanks>

For more specifics on the filtering options, have a look at the `cfoldseeker-seqs documentation <https://cfoldseeker.readthedocs.io/en/latest/guide/usage.html#extracting-gene-clusters>`_.

