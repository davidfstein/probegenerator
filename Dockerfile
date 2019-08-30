FROM debian:stable-slim

RUN apt-get update && yes|apt-get upgrade && apt-get clean all && \
    apt-get --no-install-recommends install -y wget bzip2 && \
    rm -rf /var/lib/apt/lists/* && \
    wget --no-check-certificate https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh && \
    sh Miniconda2-latest-Linux-x86_64.sh -b && \
    rm Miniconda2-latest-Linux-x86_64.sh && \
    apt-get remove -y wget bzip2

ENV PATH /root/miniconda2/bin:$PATH

RUN conda config --add channels Bioconda && \
    pip install numpy scipy scikit-learn biopython && \
    conda install bowtie2 pysam && \
    mkdir /data

COPY . /app

WORKDIR /app

ENTRYPOINT bash "$path_to_probe_generator_project/run.sh" \
                $path_to_probe_generator_project \
                $seq_path \
                $path_to_block_parse \
                $l \
                $L \
                $g \
                $G \
                $t \
                $T \
                $s \
                $F \
                $desired_spaces \
                $initiator \
                $path_to_bowtie_index \
                $bowtie_index_basename
