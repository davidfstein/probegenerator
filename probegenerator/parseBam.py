from __future__ import print_function
from argparse import ArgumentParser
from pysam import AlignmentFile

def parse_alignment_bam(file_path):
    bamfile = AlignmentFile(file_path, 'rb')
    return [read for read in bamfile.fetch()]

def extract_alignment_scores(reads):
    scores = []
    for read in reads:
        score = []
        if read.tags[0][0] == 'AS':
            score.append(read.tags[0][1])
        else:
            score.append(None)
        if len(read.tags) > 1 and read.tags[1][0] == 'XS':
            score.append(read.tags[1][1])
        else:
            score.append(None)
        scores.append(score)
    return scores
            
def write_scores_to_disk(scores):
    with open('probe_scores.txt', 'w+') as file:
        for score in scores:
            file.write(str(score) + '\n')

def main():
    userInput = ArgumentParser(description="")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-p', '--Path', action='store', required=True)
    args = userInput.parse_args()
    input_path = args.Path
    reads = parse_alignment_bam(input_path)
    scores = extract_alignment_scores(reads)
    write_scores_to_disk(scores)

if __name__ == '__main__':
    main()