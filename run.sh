#!/usr/bin/env bash

if [ -d "/data/output" ] 
then
    echo "Please remove or move the output folder from your mount directory." && exit 1
fi 
mkdir /data/output

export BOWTIE2_INDEXES=/data/${12}

fasta_files=$(/root/miniconda2/bin/python /app/probegenerator/probegenerator/parseMultifasta.py -f /data/$1)
declare -a gene_fastas=($fasta_files)
for fasta in "${gene_fastas[@]}"
do 
    /root/miniconda2/bin/python /app/OligoMiner/blockParse.py -f $fasta.fa -l $2 -L $3 -g $4 -G $5 -t $6 -T $7 -s $8 -F $9 -O -b -o ../output
    gene_name=(${fasta//\// })
    /root/miniconda2/bin/python /app/probegenerator/probegenerator/probeGenerator.py -p ../output.bed -f $fasta.fa -s ${10} -if /data/${11}
    bowtie2 -x ${13} -U ../probes_for_alignment.fa -t -f --very-sensitive -k 5 --int-quals --no-1mm-upfront --score-min L,-40,-0.6 -p 4 > "${gene_name[1]}".bam
    /root/miniconda2/bin/python /app/probegenerator/probegenerator/utils/file_copy_utils.py -i /data/${11} -n "${gene_name[1]}"
    /root/miniconda2/bin/python /app/probegenerator/probegenerator/parseBam.py -p ${gene_name[1]}/${gene_name[1]}_probes.csv -p2 ${gene_name[1]}/${gene_name[1]}.bam -i /data/${11}
done