fasta_files=$(python $1/probegenerator/parseMultifasta.py -f $2)
declare -a arr=($fasta_files)
export BOWTIE2_INDEXES=${18}
for fasta in "${arr[@]}"
do 
    # Consider turning off overlap mode of blockParse
    python $3 -f $fasta.fa -l $4 -L $5 -g $6 -G $7 -t $8 -T $9 -s ${10} -F ${11} -O -b -o ../output
    python $1/probegenerator/probeGenerator.py -p ../output.bed -s ${12} -i ${13} -l ${14} --LeftSpacer ${15} -r ${16} --RightSpacer ${17}
    bowtie2 -x ${19} -U ../probes_for_alignment.fa -f --very-sensitive > ../output.bam
    python $1/probegenerator/parseBam.py -p ../output.bam
    python $1/probegenerator/probeWriter.py --TagFile ../probe_scores.txt --Probes ../probes_with_meta.txt
done

