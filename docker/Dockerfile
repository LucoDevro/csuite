FROM vanallenlab/miniconda:3.12

LABEL description="csuite - Streamlined workflows for query-based gene cluster mining"
LABEL org.opencontainers.image.authors="lucas.devrieze@kuleuven.be"

# Use bash as shell
SHELL ["/bin/bash", "-c"]

# Install csuite and add environment to PATH
RUN conda install -c bioconda -c conda-forge csuite -y
ENV PATH=/usr/miniconda3/envs/csuite/bin/:$PATH
