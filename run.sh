#!/usr/bin/env bash

export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION

if [ -d "/data/output" ] 
then
    echo "Please remove or move the output folder from your mount directory." && exit 1
fi 
mkdir /data/output

export BOWTIE2_INDEXES=/data/${12}

python /app/probegenerator/probegenerator/parseMultifasta.py -f /data/$1
while read -r fasta
do 
    python /app/OligoMiner/blockParse.py -f $fasta.fa -l $2 -L $3 -g $4 -G $5 -t $6 -T $7 -s $8 -F $9 -O -b -o ../output
    gene_name=(${fasta//\// })
    python /app/probegenerator/probegenerator/probeGenerator.py -p ../output.bed -f $fasta.fa -s ${10} -if /data/${11}    

    # Ouput clean with lda model or unique alignment
    if [ "${14}" == "true" ]; then
        bowtie2 -x ${13} -U /app/probes_for_alignment.fastq -t -k 2 --local -D 20 -R 3 -N 1 -L 20 -i C,4 --score-min G,1,4 -S "${gene_name[1]}".sam
        python /app/OligoMiner/outputClean.py -l -f "${gene_name[1]}".sam -o "${gene_name[1]}"
    else
        bowtie2 -x ${13} -U /app/probes_for_alignment.fastq -t -k 100 --very-sensitive-local -S "${gene_name[1]}".sam
        python /app/OligoMiner/outputClean.py -u -f "${gene_name[1]}".sam -o "${gene_name[1]}"
    fi

    python /app/probegenerator/probegenerator/utils/file_copy_utils.py -i /data/${11} -n "${gene_name[1]}" 
    python /app/probegenerator/probegenerator/parseBam.py -p ${gene_name[1]}/${gene_name[1]}_probes.csv -p2 ${gene_name[1]}/${gene_name[1]} -i /data/${11} 
done < /app/names.txt

zip -r /data/results.zip /data/output

if [ ! -z "${15}" ]
then
    python /app/probegenerator/probegenerator/utils/mail_utils.py -r ${15} -j ${16}
fi

if [ $? != 0 ];
then
    exit 1
fi