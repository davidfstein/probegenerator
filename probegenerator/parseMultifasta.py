from __future__ import print_function
from argparse import ArgumentParser
from collections import namedtuple
from Bio import SeqIO
from utils.file_writer_utils import write_fasta

def multifasta_to_list_of_fasta(multifasta_path):
    with open(multifasta_path, 'rU') as multifasta:
        return [record for record in SeqIO.parse(multifasta, 'fasta')]

def main():
    userInput = ArgumentParser(description="Requires a fasta file or multifasta file as input. If file is multifasta, the file is split "
                                                    + "into mulitple single entry fasta files and the new fasta files are written to the current directory. "
                                                    + "Returns a list of resulting file names for passing to downstream tools.")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-f', '--file', action='store', required=True,
                                help='The FASTA file for splitting')
    args = userInput.parse_args()
    inputFile = args.file
    
    records = multifasta_to_list_of_fasta(inputFile)
    print(*write_fasta(records))

if __name__ == '__main__':
    main()