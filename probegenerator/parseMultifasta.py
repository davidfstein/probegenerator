from __future__ import print_function
from argparse import ArgumentParser
from collections import namedtuple

def write_to_separate_fasta_files(fasta_entries):
    file_names = []
    for entry in fasta_entries:
        file_names.append(entry.name)
        with open(entry.name + ".fa", 'w+') as file:
            file.write(">" + entry.name + "\n" + entry.sequence)
    return file_names

def multifasta_to_sequence_list(multifasta):
    FastaEntry = namedtuple('FastaEntry', 'name sequence')
    entries = []
    header_indices = [i for i in range(0,len(multifasta)) if is_header(multifasta[i])]
    for i in range(0, len(header_indices)):
        if i == len(header_indices) - 1:
            seq = concat_lines(multifasta[header_indices[i] + 1:])
            gene_name = gene_name_from_header(multifasta[header_indices[i]]).strip('\n')
            entries.append(FastaEntry(name=gene_name, sequence=seq))
        else:
            header_index = header_indices[i]
            next_header_index = header_indices[i+1]
            seq = concat_lines(multifasta[header_index + 1:next_header_index])
            gene_name = gene_name_from_header(multifasta[header_index]).strip('\n')
            entries.append(FastaEntry(name=gene_name, sequence=seq))
    return entries

def concat_lines(lines):
    concatted_line = ''
    for line in lines:
        concatted_line += line
    return concatted_line

def gene_name_from_header(line):
    return line[1:].split(' ')[0]

def is_header(line):
    return '>' in line

def main():
    userInput = ArgumentParser(description="Requires a fasta file or multifasta file as input. If file is multifasta, the file is split "
                                                    + "into mulitple single entry fasta files and the new fasta files are written to the current directory. "
                                                    + "Returns a list of resulting file names for passing to downstream tools.")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-f', '--file', action='store', required=True,
                                help='The FASTA file for splitting')
    args = userInput.parse_args()
    inputFile = args.file
    
    with open(inputFile) as file:
        fasta_entries = multifasta_to_sequence_list(file.readlines())
        print(*write_to_separate_fasta_files(fasta_entries))

if __name__ == '__main__':
    main()