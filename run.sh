fasta_files=$(python $1 -f $2)
declare -a arr=($fasta_files)
export BOWTIE2_INDEXES=/app/M21-transcriptome/
for fasta in "${arr[@]}"
do 
    # Consider turning off overlap mode of blockParse
    python $3 -f "$fasta.fa" -l $4 -L $5 -g $6 -G $7 -t $8 -T $9 -s ${10} -F ${11} -O -b -o ${12}
    python ${13} -p ${14} -s ${15} -i ${16} -l ${17} --LeftSpacer ${18} -r ${19} --RightSpacer ${20}
    bowtie2 -x M21-transcriptome -U ../probes_for_alignment.fa -f --very-sensitive > ../output.bam
    python ./probegenerator/probegenerator/parseBam.py -p ../output.bam
    python ./probegenerator/probegenerator/probeWriter.py --TagFile ../probe_scores.txt --Probes ../probes_with_meta.txt
done

