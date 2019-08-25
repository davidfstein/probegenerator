#!/usr/bin/env bash

gene_paths=$(find $1 -type d -print)
declare -a arr=($gene_paths)
for gene_path in "${arr[@]}"
do 
    if [ ! -z "$gene_path" ]
    then
        gene_name=$(echo ${gene_path} | sed 's:.*/::')
        output=$(python probegenerator/parseBam.py -p ${gene_path}/${gene_name}_probes.csv -p2 ${gene_path}/${gene_name}.bam -i $2 )
        mv $output ${gene_path}
    fi
done