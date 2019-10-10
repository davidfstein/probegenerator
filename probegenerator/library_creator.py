from __future__ import print_function
from argparse import ArgumentParser
from utils import file_reader_utils
import os
import csv
import constants


def append_library_name(sublibrary_name, sublibrary_path):
    '''
    Add sublibrary name to the header of the sublibrary fasta file.
    '''
    with open(sublibrary_path, "w") as sub_fasta:
        data = sub_fasta.readlines()
        sub_fasta.write(sublibrary_name + '\n')
        sub_fasta.write(data)


def compile_sublibrary_fasta(sublibrary_spec_path):
    '''
    Concatanate probe sequences from all individual genes to a single fasta file for each 
    sublibrary.
    '''
    with open(sublibrary_spec_path) as sublibrary_spec:
        data = csv.DictReader(sublibrary_spec)
        for row in data:
            with open(os.path.join(constants.TEST_BASE_DIR, 'Library', row['Subpool']) + '.fa', 'w') as subpool:
                subpool.write(row['Subpool'] + '\n')
                for initiator, gene in row.items():
                    if initiator == 'Subpool':
                        continue
                    with open(os.path.join(constants.TEST_BASE_DIR, initiator, gene.capitalize(), gene.capitalize() + '.fasta')) as gene:
                        for line in gene.readlines():
                            subpool.write(line)

def clean_sublibrary(sublibrary_path):
    '''
    Write new sublibrary fasta files without ">".
    '''
    cleaned_lines = []
    with open(sublibrary_path, 'r') as sublibrary:
        cleaned_lines = [line for line in sublibrary.readlines() if not line.lstrip().startswith(">")]

    clean_file_path = sublibrary_path[::-1].split('.', 1)[1][::-1]
    with open(clean_file_path + '_clean.fa', 'w') as clean_sublibrary:
        for line in cleaned_lines:
            clean_sublibrary.write(line)


def attach_primers(sublibrary_path, nt_primer, nb_primer, header_line=True):
    with open(sublibrary_path) as sublibrary:
        data = sublibrary.readlines()
        probes_with_primers = []
        for i in range(0, len(data)):
            #Skip first line if it is a header
            if header_line and i == 0:
                continue
            probes_with_primers.append(nt_primer + data[i].strip('\n') + nb_primer)
        return probes_with_primers            

def get_primer_sequence(primer_data, primer_id):
    for row in primer_data:
        if row['plate_position'] == primer_id:
            return row['sequence']

def concatenate_sublibraries(sublibrary_names):

    sublibrary_sequences = []
    for name in sublibrary_names:
        with open(os.path.join(constants.TEST_BASE_DIR, 'Library', name + '_primers.fa')) as sublibrary:
            sublibrary_sequences.append(sublibrary.readlines())

    with open(os.path.join(constants.TEST_BASE_DIR, 'Library_order.txt'), 'w') as order:
        for sublibrary in sublibrary_sequences:
            for sequence in sublibrary:
                order.write(sequence)

### Order of events ###
# Combine fasta from genes into a single file for each sublibrary
# Append library names to sublibrary fasta files
# Remove > header lines from sublibrary fasta files
# Attach appropriate primers to the sublibraries
# Add reverse complements of all sequences from all sublibraries to a final file for ordering

if __name__ == '__main__':
    userInput = ArgumentParser(description="")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-s', '--SubpoolIndex', action='store', required=True)
    requiredNamed.add_argument('-p', '--PrimerIndex', action='store', required=True)
    requiredNamed.add_argument('-nt', '--NtPrimers', action='store', required=True)
    requiredNamed.add_argument('-nb', '--NbPrimers', action='store', required=True)
    args = userInput.parse_args()
    subpool_index_path = args.SubpoolIndex
    primer_index_path = args.PrimerIndex
    nt_path = args.NtPrimers
    nb_path = args.NbPrimers

    # Combine fasta from genes into a single file for each sublibrary
    # Append library names to sublibrary fasta files
    compile_sublibrary_fasta(subpool_index_path)

    # Removing > from sublibrary fastas
    (_, _, filenames) = next(os.walk(os.path.join(constants.TEST_BASE_DIR, 'Library')))
    for filename in filenames:
        clean_sublibrary(os.path.join(constants.TEST_BASE_DIR, 'Library', filename))

    primer_indexes = file_reader_utils.read_delimited_file_as_dict_list(primer_index_path)
    
    # Attach primers to cleaned sublibrary fasta sequences
    nt_primer_data = file_reader_utils.read_delimited_file_as_dict_list(nt_path)
    nb_primer_data = file_reader_utils.read_delimited_file_as_dict_list(nb_path)
    for index in primer_indexes:
        nt_primer = get_primer_sequence(nt_primer_data, index['Nt'])
        nb_primer = get_primer_sequence(nb_primer_data, index['Nb'])
        library = index['sublibraries']
        library_with_primers = attach_primers(os.path.join(constants.TEST_BASE_DIR, 'Library', library + '_clean.fa'), nt_primer, nb_primer)
        with open(os.path.join(constants.TEST_BASE_DIR, 'Library', library + '_primers.fa'), 'w') as pool_with_primers:
            for line in library_with_primers:
                pool_with_primers.write(line + '\n')

    # Append all sequences to order file
    sublibrary_names = [row['sublibraries'] for row in primer_indexes]
    concatenate_sublibraries(sublibrary_names)