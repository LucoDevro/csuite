Installation
============

.. note::
   
   Supported Python versions are 3.12, 3.13 and 3.14.

.. important::

   Don't forget to download the UniProt ID mapping table (``uniprot_kegg_genpept.gz``) from the `latest cfoldseeker release <https://github.com/LucoDevro/cfoldseeker/releases/latest>`_ if you'd like to run a remote structure-based search.


Conda (recommended)
-----------------------

This is the recommended and most straightforward way to install csuite. It should work on any Linux or MacOS system. Create a fresh conda environment as well to keep it from meddling with your other tools. It is directly installable from Bioconda.

.. code-block:: bash

	conda create -n csuite -c bioconda -c conda-forge csuite

or by using the conda `yml` environment file in this repo.

.. code-block:: bash

	conda env create -f env.yml

Then start using it by activating the conda environment.

.. code-block:: bash

	conda activate csuite

Docker
-------

csuite is also available as a Docker image from DockerHub. This is one of the recommended ways to run csuite on Windows (the other one being running it using Windows' WSL feature).

.. code-block:: bash

	docker pull lucodevro/csuite

There is no entrypoint set up so running csuite requires prepending your csuite command with the appropriate Docker commands.

.. code-block:: bash

	docker run lucodevro/csuite -v <some-input-file-or-folder>:<path-you-want-it-inside-the-container> csuite [workflow] [-<flags>] [arguments]

GitHub
-------

Alternatively, it is possible to install the latest semi-stable development version by cloning this repository and running the following command at the root of your local copy of this repository.

.. code-block:: bash

	pip install .

PyPi
------

csuite is also installable from PyPi using pip, yet we do not recommend using this approach as several core dependencies are not available from PyPi, and therefore should be installed in another way. So either make sure you have installed it separately, or use one of the other installation options.

.. code-block:: bash

	pip install csuite

.. warning::
   
   We do not recommend using this approach as key non-Python dependencies are not available from PyPi and therefore should be installed separately.

