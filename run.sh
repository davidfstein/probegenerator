#!/usr/bin/env bash

fasta_files=$(python $1/probegenerator/parseMultifasta.py -f $2)
declare -a arr=($fasta_files)
export BOWTIE2_INDEXES=${14}
for fasta in "${arr[@]}"
do 
    python $3 -f $fasta.fa -l $4 -L $5 -g $6 -G $7 -t $8 -T $9 -s ${10} -F ${11} -O -b -o ../output
    splitFilePathArr=(${fasta//\// })
    python $1/probegenerator/probeGenerator.py -p ../output.bed -f $fasta.fa -s ${12} -if ${13}
    bowtie2 -x ${15} -U ../probes_for_alignment.fa -t -f --very-sensitive -k 5 --int-quals --no-1mm-upfront --score-min L,-40,-0.6 -p 4 > "${splitFilePathArr[1]}".bam
    python $1/probegenerator/file_copy_utils.py -i ${13} -n "${splitFilePathArr[1]}".bam
done
