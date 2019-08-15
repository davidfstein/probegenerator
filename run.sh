fasta_files=$(python $1/probegenerator/parseMultifasta.py -f $2)
declare -a arr=($fasta_files)
export BOWTIE2_INDEXES=${18}
for fasta in "${arr[@]}"
do 
    # Consider turning off overlap mode of blockParse
    python $3 -f $fasta.fa -l $4 -L $5 -g $6 -G $7 -t $8 -T $9 -s ${10} -F ${11} -O -b -o ../output
    splitFilePathArr=(${fasta//\// })
    mkdir "${splitFilePathArr[1]}"
    python $1/probegenerator/probeGenerator.py -p ../output.bed -f $fasta.fa -s ${12} -i ${13} -l ${14} --LeftSpacer ${15} -r ${16} --RightSpacer ${17}
    bowtie2 -x ${19} -U ../probes_for_alignment.fa -t -f --very-sensitive -k 5 --int-quals --no-1mm-upfront --score-min L,-40,-0.6 -p 4 > ./"${splitFilePathArr[1]}"/"${splitFilePathArr[1]}".bam
    mv "${splitFilePathArr[1]}"_probes.csv ./"${splitFilePathArr[1]}"/
done

