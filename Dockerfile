FROM python:2.7-slim

COPY . /app

WORKDIR /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT bash "$path_to_probe_generator_project/run.sh" \
                "$path_to_probe_generator_project/probegenerator/parseMultifasta.py" \
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
                ../output \ 
                "$path_to_probe_generator_project/probegenerator/probeGenerator.py" \
                ../output.bed \
                $desired_spaces \
                $initiator \
                $left_init_seq \
                $left_spacer \
                $right_init_seq \
                $right_spacer