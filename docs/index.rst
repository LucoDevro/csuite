.. csuite documentation master file, created by
   sphinx-quickstart on Tue Apr 14 13:00:12 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

csuite
=======================================

**Welcome to csuite's documentation!**

|docs|
|conda|
|bioconda|
|docker|
|pypi|

.. |docs| image:: https://img.shields.io/readthedocs/csuite-miner/latest?style=flat-square&maxAge=600&logo=readthedocs
   :target: https://csuite-mining.readthedocs.io/en/latest/

.. |bioconda| image:: https://img.shields.io/conda/vn/bioconda/csuite?style=flat-square&maxAge=3600&logo=anaconda
   :target: https://anaconda.org/bioconda/csuite

.. |docker| image:: https://img.shields.io/docker/v/lucodevro/csuite?sort=semver&label=docker&logo=docker
   :target: https://hub.docker.com/r/lucodevro/csuite

.. |pypi| image:: https://img.shields.io/pypi/v/csuite?sort=semver&logo=pypi
   :target: https://pypi.org/project/csuite/

.. |conda| image:: https://img.shields.io/conda/dn/bioconda/csuite.svg
   :target: https://anaconda.org/bioconda/csuite/files

*csuite: Streamlined workflows for query-based gene cluster mining.*

The **csuite** provides easy-to-use one-go commands for query-based gene cluster mining. It wraps several mining and processing tools into end-to-end workflows, removing the sizeable file and settings plumbing overhead.

The **csuite** bundles the following tools
	- **cblaster** - sequence similarity-based gene cluster mining
	- **cfoldseeker** - protein structure similarity-based gene cluster mining
	- **CAGEcleaner** - hit redundancy removal with respect for both gene cluster and host diversity
	- **clinker** - interactive gene cluster visualisations.

.. tip::

   The **csuite** workflows are similar in design philosophy as **MMseqs2**'s and **FoldSeek**'s ``easy-*`` combo commands!

   For more fine-grained settings, you can still run the member tools of the **csuite** separately. You can just call them inside **csuite**'s conda environment or Docker container.

The **csuite** currently supports the workflows listed below.

1. ``local_struc_derep``: Local structure-based search with hit dereplication
	- Local context database construction using ``cfoldseeker-cds``
	- Structure-based search in local mode using ``cfoldseeker``
	- Hit dereplication in local mode using ``CAGEcleaner``
2. ``local_struc``: Local structure-based search
	- Local context database construction using ``cfoldseeker-cds``
	- Structure-based search in local mode using ``cfoldseeker``
3. ``remote_struc_derep``: Remote structure-based search with hit dereplication
	- Structure-based search in remote mode using ``cfoldseeker``
	- Hit dereplication in remote mode using ``CAGEcleaner``
4. ``remote_struc``: Remote structure-based search
	- Structure-based search in remote mode using ``cfoldseeker``
5. ``local_seq_derep``: Local sequence-based search with hit dereplication
	- Sequence database construction using ``cblaster makedb``
	- Sequence-based search in local mode using ``cblaster search``
	- Hit dereplication in local mode using ``CAGEcleaner``
6. ``local_seq``: Local sequence-based search
	- Sequence database construction using ``cblaster makedb``
	- Sequence-based search in local mode using ``cblaster search``
7. ``remote_seq_derep``: Local sequence-based search with hit dereplication
	- Sequence-based search in remote mode using ``cblaster search``
	- Hit dereplication in remote mode using ``CAGEcleaner``
8. ``remote_seq``: Remote sequence-based search
	- Sequence-based search in remote mode using ``cblaster search``
9. ``derep``: Hit dereplication
	- Hit dereplication using ``CAGEcleaner`` (unified interface for all search modes)
10. ``report``: Generate reports for an existing session
	- Generating summary, plot and binary table files using ``cblaster``
	- Alignment visualisation using ``clinker``
11. ``remote_extract``: Export cluster Genbank files from a remote mode search session
	- Generate cluster Genbank files for an existing session using ``cblaster extract_clusters``
12. ``local_extract``: Export cluster Genbank files from a local mode search session
	- Generate cluster Genbank files for an existing session using ``cfoldseeker-seqs``

References and citations
=========================

If you find ``csuite`` useful, please cite our manuscript:

::

	In preparation


Our member tools rely heavily on the following tools, so please give these proper credit as well:

::

    Gilchrist, C.L.M., Booth, T.J., van Wersch, B., van Grieken, L., Medema, M.H., & Chooi, Y-H. (2021). cblaster: a remote search tool for rapid identification and visualisation of homologous gene clusters. Bioinformatics Advances, https://doi.org/10.1093/bioadv/vbab016
    van Kempen, M., Kim, S.S., Tumescheit, C., Mirdita, M., Lee, J., Gilchrist, C.L.M., Söding, J., Steinegger, M. (2024). Fast and accurate protein structure search with Foldseek. Nature Biotechnology, 42, https://doi.org/10.1038/s41587-023-01773-0
    Steinegger, M., & Söding, J. (2017). MMseqs2 enables sensitive protein sequence searching for the analysis of massive data sets. Nature Biotechnology, 35, https://doi.org/10.1038/nbt.3988
    Huckvale, E., Moseley, H.N.B. (2023). kegg_pull: a software package for the RESTful access and pulling from the Kyoto Encyclopedia of Gene and Genomes. BMC Bioinformatics, 24(78), https://doi.org/10.1186/s12859-023-05208-0
    Salamzade, R., & Kalan, L. R. (2025). skDER and CiDDER: two scalable approaches for microbial genome dereplication. Microbial Genomics, 11(7), https://doi.org/10.1099/mgen.0.001438
    Shaw, J., & Yu, Y. W. (2023). Fast and robust metagenomic sequence comparison through sparse chaining with skani. Nature Methods, 20(11), 1661–1665. https://doi.org/10.1038/s41592-023-02018-3


.. toctree::
   :caption: User Guide
   :maxdepth: 2

   guide/install
   guide/usage


.. toctree::
   :caption: API Reference
   :maxdepth: 1

   api_ref

