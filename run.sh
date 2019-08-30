#!/usr/bin/env bash

mkdir /data/output
fasta_files=$(python /app/probegenerator/probegenerator/parseMultifasta.py -f $1)
declare -a arr=($fasta_files)
export BOWTIE2_INDEXES=${12}
for fasta in "${arr[@]}"
do 
    python /app/OligoMiner/blockParse.py -f $fasta.fa -l $2 -L $3 -g $4 -G $5 -t $6 -T $7 -s $8 -F $9 -O -b -o ../output
    splitFilePathArr=(${fasta//\// })
    python /app/probegenerator/probegenerator/probeGenerator.py -p ../output.bed -f $fasta.fa -s ${10} -if ${11}
    bowtie2 -x ${13} -U ../probes_for_alignment.fa -t -f --very-sensitive -k 5 --int-quals --no-1mm-upfront --score-min L,-40,-0.6 -p 4 > "${splitFilePathArr[1]}".bam
    python /app/probegenerator/probegenerator/file_copy_utils.py -i ${11} -n "${splitFilePathArr[1]}"
done
