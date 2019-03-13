FROM python:2.7-slim

COPY . /app

WORKDIR /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT python $path_to_block_parse -f $seq_path -l $l -L $L -g $g -G $G -t $t -T $T -s $s -F $F -O -b -R -o $bed_output_path && \
           python ./probegenerator/probeGenerator.py -p "$bed_output_path.bed" -s 3