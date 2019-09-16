from __future__ import print_function
from argparse import ArgumentParser
from orf_finder import find_start_codons, find_longest_orf
from utils.reverse_complement import reverseComplement
from utils.initiator_utils import parse_initiators
import utils.file_writer_utils as file_writer_utils
import constants
import csv
import os

def read_probes(probe_candidates):
    with open(probe_candidates) as probes:
        return [line.rstrip("\n").split("\t") for line in probes if len(line.rstrip("\n").split("\t")) > 0]

def filter_probes_by_spaces(probes, desired_spaces):
    '''
    Filter probes without at least the desired number of bases in between their indices.
    '''
    filtered_probes = []
    probe_end = 0
    for probe in probes:
        if int(probe[1]) >= probe_end:
            filtered_probes.append(probe)
            probe_end = int(probe[2]) + desired_spaces
    return filtered_probes


def get_probe_pairs(sequences, desired_spaces): 
    '''
    Seperate probes into pairs. Probes in a pair must be seperated by exactly desired_spaces
    number of base pairs.
    '''
    if not sequences:
        raise Exception("Empty sequence list")
    
    pairs = []
    previous_sequence = sequences[0]
    for sequence in sequences[1:]:
        cur_start = int(sequence[1])
        prev_end = int(previous_sequence[2])
        if pairs and previous_sequence in pairs[-1]:
            previous_sequence = sequence
            continue
        if (cur_start - prev_end == desired_spaces):
            pairs.append([previous_sequence, sequence])
        previous_sequence = sequence    

    return pairs

def create_pair_metadata(pairs, orf_start, orf_length, initiator_name, left_initiator_seq, left_initiator_spacer, 
                         right_initiator_seq, right_initiator_spacer):
    '''
    Create metadata for each probe. Metadata includes the reverse complement sequence, initiator name and sequence,
    a boolean denoting the placement of the probe in or out of the longest ORF, the number of spaces from the previous probe,
    the final probe name, the set number, and the final probe sequence.
    '''
    last_seq_end = 0
    pair_metadata = []
    for index in range(0, len(pairs)):
        left = pairs[index][0]
        left_seq_reverse_complement = reverseComplement(left[3])
        left_in_orf = is_probe_in_orf(int(left[1]), len(left[3]), orf_start, orf_length)
        right = pairs[index][1]
        right_seq_reverse_complement = reverseComplement(right[3])
        right_in_orf = is_probe_in_orf(int(right[1]), len(right[3]), orf_start, orf_length)
        left_space = int(left[1]) - int(last_seq_end)
        right_space = int(right[1]) - int(left[2])
        set_num = index + 1
        left_final_name = left[0] + "_" + str(set_num) + "." + str(1) + "_" + initiator_name
        right_final_name = right[0] + "_" + str(set_num) + "." + str(2) + "_" + initiator_name 
        left_final_probe = left_initiator_seq + left_initiator_spacer + left_seq_reverse_complement
        right_final_probe = right_seq_reverse_complement + right_initiator_spacer + right_initiator_seq
        left_meta = [left_space, set_num, left_seq_reverse_complement, '_' + initiator_name, 
                     left_final_name, left_initiator_seq, left_initiator_spacer, 
                     left_seq_reverse_complement, left_final_probe, left_in_orf]
        right_meta = [right_space, set_num, right_seq_reverse_complement, '_' + initiator_name, 
                      right_final_name, right_seq_reverse_complement, right_initiator_spacer, 
                      right_initiator_seq, right_final_probe, right_in_orf]
        pair_metadata.append([left_meta, right_meta])
        last_seq_end = right[2]
    return pair_metadata

def append_metadata_to_probes(probes, metadata):
    '''
    Add corresponding metadata to individual probes in each probe pair.
    '''
    i = 0
    probes_with_meta = []
    while i < len(probes) and i < len(metadata):
        first = probes[i][0] + metadata[i][0]
        second = probes[i][1] + metadata[i][1]
        probes_with_meta.append([first, second])
        i += 1
    return probes_with_meta

def is_probe_in_orf(probe_start, probe_length, orf_start, orf_length):
    '''
    Determine if a probe is entirely inside an open reading frame.
    '''
    return probe_start >= orf_start and probe_start + probe_length <= orf_start + orf_length 

def main():
    userInput = ArgumentParser(description="Requires a path to a bed file from which to read probes. Takes an integer value to determine "
                                            + "the number of spaces between probes in a pair. Also takes initiator sequences and an initiator spacer "
                                            + "for appending to the probes. Outputs a csv containing candidate probe pairs.")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-p', '--Path', action='store', required=True,
                                help='The bed file with probe sequences')
    requiredNamed.add_argument('-f', '--Fasta', action='store', required=True,
                                help='The fasta file with the gene of interest')
    requiredNamed.add_argument('-s', '--Spaces', action='store', required=True,
                                help="Desired number of spaces between probes in a pair")
    requiredNamed.add_argument('-if', '--InitiatorFile', action='store', required=True,
                                help="File containing initiators.")
    args = userInput.parse_args()
    input_path = args.Path
    fasta = args.Fasta
    desired_spaces = int(args.Spaces)
    initiator_file = args.InitiatorFile

    lines = []
    with open(fasta) as file:
        lines = [line.strip('\n') for line in file.readlines()][1:]
    sequence = ''
    for line in lines:
        sequence += line

    start_codons = find_start_codons(sequence)
    start_orf, orf_length = find_longest_orf(sequence, start_codons)

    candidate_probes = read_probes(input_path)
    filtered_probes = filter_probes_by_spaces(candidate_probes, desired_spaces)
    pairs = get_probe_pairs(filtered_probes, desired_spaces)
    file_writer_utils.write_probes_for_alignment_fasta(pairs, desired_spaces)

    initiators = parse_initiators(initiator_file)

    pairs_with_meta = {}
    for initiator in initiators:
        pair_meta = create_pair_metadata(pairs, start_orf, orf_length, *initiator)
        pairs_with_meta[initiator[0]] = append_metadata_to_probes(pairs, pair_meta)
    
    for initiator in pairs_with_meta:
        sequence_name = pairs[0][0][0].split(" ")[0]
        if not os.path.isdir(os.path.join(constants.OUTPUT_BASE_DIR, initiator)):
            os.mkdir(os.path.join(constants.OUTPUT_BASE_DIR, initiator))
        if not os.path.isdir(os.path.join(constants.OUTPUT_BASE_DIR, initiator, sequence_name)):
            os.mkdir(os.path.join(constants.OUTPUT_BASE_DIR, initiator, sequence_name))
        file_writer_utils.write_probes_to_csv(pairs_with_meta[initiator], os.path.join(constants.OUTPUT_BASE_DIR, initiator, sequence_name))

if __name__ == '__main__':
    main()
