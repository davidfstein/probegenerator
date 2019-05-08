fasta_files=$(python $1 -f $2)
declare -a arr=($fasta_files)
for fasta in "${arr[@]}"
do 
    python $3 -f "$fasta.fa" -l $4 -L $5 -g $6 -G $7 -t $8 -T $9 -s ${10} -F ${11} -O -b -R -o ${12} && \
    python ${13} -p ${14} -s ${15} -i ${16} -l ${17} --LeftSpacer ${18} -r ${19} --RightSpacer ${20}
done

