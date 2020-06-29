from __future__ import print_function
from argparse import ArgumentParser
from collections import namedtuple
from Bio import SeqIO
from utils.file_writer_utils import write_fasta

def multifasta_to_list_of_fasta(multifasta_path):
    '''
    Split a fasta file with multiple entries into individual records and return the records as a list.
    '''
    with open(multifasta_path, 'rU') as multifasta:
        return [record for record in SeqIO.parse(multifasta, 'fasta')]

def main():
    '''
    Split a fasta file into invidual records. Write each record to disk as an individual fasta file.
    Print the individual fasta file names to standard out. 
    '''
    userInput = ArgumentParser(description="Requires a fasta file or multifasta file as input. If file is multifasta, the file is split "
                                                    + "into mulitple single entry fasta files and the new fasta files are written to the current directory. "
                                                    + "Prints a list of resulting file names for passing to downstream tools.")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-f', '--file', action='store', required=True,
                                help='The FASTA file for splitting')
    args = userInput.parse_args()
    inputFile = args.file

    lines = []
    with open(inputFile, 'r') as original:
        lines = original.readlines()

    path = inputFile.split('/')[-1]
    with open('/data/prepend' + path, 'w+') as prepended:
        prepended.write("\n")
        for line in lines:
            line = ''.join([i if ord(i) < 128 else '' for i in line])
            prepended.write(line)
    
    records = multifasta_to_list_of_fasta('/data/prepend' + path)
    names = write_fasta(records)
    with open('/app/names.txt', 'w+') as f:
        for name in names:
            f.write(name + '\n')

if __name__ == '__main__':
    main()