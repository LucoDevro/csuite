Getting started
================

A csuite workflow wraps multiple tools into one streamlined pipeline. We optimised for nicely integraded workflows that starts from as many raw inputs as possible (fasta files, protein structures), but are not too time- or resource-intensive to run in one go. Remote runs nicely allow for this as much of the heavy lifting has been outsourced to a webserver. However, for local runs, we kept heavy upstream tasks that are not directly related to the search itself out of the pipeline. These can be run on HPC systems instead.

.. tip::

   For documentation of all options, we refer to the documentation of the csuite member tools (`cblaster <https://cblaster.readthedocs.io/en/latest/>`_,  `cfoldseeker <https://cfoldseeker.readthedocs.io/en/stable/>`_,  `CAGEcleaner <https://cagecleaner.readthedocs.io/en/stable/>`_).


Remote runs
------------

Remote runs are the easiest to get started.

For **structure-based searches** against the AFDB50 database at default settings, run the ``remote_struc`` workflow.

.. code-block:: bash

	csuite remote_struc -q <query-folder> -uma <UniProt-ID-mapping-table>

To **include hit dereplication** at default settings (genome-based at 99% identity and 80% coverage), run the ``remote_struc_derep`` workflow.

.. code-block:: bash

	csuite remote_struc_derep -q <query-folder> -uma <UniProt-ID-mapping-table>

**Sequence-based searches** against the default database (NCBI nr) at default search settings can be done using the ``remote_seq`` workflow.

.. code-block:: bash

	csuite remote_seq -q <query-folder>

To **include a region-based hit dereplication** with sequence margins of 5 kb, run the ``remote_seq_derep`` workflow.

.. code-block:: bash

	csuite remote_seq_derep -q <query-folder> --derep-method regions -m 5000

In any case, run the ``output`` workflow afterwards to **export typical cblaster-like outputs** from the newly generated session file.

.. code-block:: bash

	csuite output -s <session-file>


Local runs
-----------

**Local sequence-based runs** are fully covered starting from the fasta files. For example, to run a local sequence-based search with default hit dereplication, run the ``local_seq_derep`` workflow. This will construct a cblaster genome database and search your query sequences against it.

.. code-block:: bash

	csuite local_seq_derep -q <query-fasta> -g <target-genomes>

**Local structure-based searches** still require some time- and resource-intensive tasks to be done beforehand. This is the case for all structure-based workflows such as generating a target protein structure database using ProstT5, or preclustering your target database using MMseqs2.

For example, to run a local structure-based search against a preclustered database, you need to execute a MMseqs2 clustering and then generate protein structures for the cluster representatives using ProstT5 via FoldSeek.

.. tip::

	For a thorough walk-through of the necessary prior work for local structure-based searches with preclustering, check out the `cfoldseeker tutorial <https://cfoldseeker.readthedocs.io/en/stable/guide/tutorial.html>`_.


.. warning::

	MMseqs2 clustering and ProstT5 protein structure generation are computationally heavy tasks! Consider moving to an HPC environment (with GPUs) for these tasks.

For example, for a local structure-based search against a preclustered database of NCBI-sourced proteomes with default hit genome-based dereplication, this might look like below.

.. code-block:: bash

	# prior work
	mmseqs easy-linclust <query-folder>/*.faa clustered tmp
	foldseek createdb clustered_rep_seq.fasta clustered_rep_struc_DB --prostt5-model <prostt5-weights>

	# search itself
	csuite local_struc_derep \
	-q <query-folder> \
	--context-input <path-to-target-ncbi-gffs> \
	--context-parsing-mode ncbi-gff \
	--search-mode local_clustered \
	-ldb clustered_rep_struc_DB 
	-scl clustered_cluster.tsv \
	--derep-method genomes \
	-g <path-to-target-ncbi-genomes>

	# export outputs from session
	csuite output -s filtered_session.json


