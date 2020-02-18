FROM debian:stable-slim

RUN apt-get update && yes|apt-get upgrade && apt-get clean all && \
    apt-get --no-install-recommends install -y wget bzip2 unzip zip && \
    rm -rf /var/lib/apt/lists/* && \
    wget --no-check-certificate https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh && \
    sh Miniconda2-latest-Linux-x86_64.sh -b && \
    rm Miniconda2-latest-Linux-x86_64.sh && \
    apt-get remove -y wget bzip2 && \
    apt-get autoremove -y

ENV PATH /root/miniconda2/bin:$PATH

RUN conda config --add channels Bioconda && \
    pip install numpy scipy scikit-learn sendgrid && \
    conda install bowtie2 pysam biopython && \
    conda install -c conda-forge awscli && \
    mkdir /data 

COPY . /app

WORKDIR /app

ENTRYPOINT bash /app/probegenerator/run.sh \
                $seq_path \
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
                $bowtie_index_basename \
                $fetch \
                $AWS_ACCESS_KEY_ID \
                $AWS_SECRET_ACCESS_KEY \
                $AWS_DEFAULT_REGION
