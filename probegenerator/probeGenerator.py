from argparse import ArgumentParser
from reverseComplement import reverseComplement
import probeWriter

def read_probes(probe_candidates):
    with open(probe_candidates) as probes:
        return [line.rstrip("\n").split("\t") for line in probes if len(line.rstrip("\n").split("\t")) > 0]

def filter_probes_by_spaces(probes, desired_spaces):
    filtered_probes = []
    probe_end = 0
    for probe in probes:
        if int(probe[1]) >= probe_end:
            filtered_probes.append(probe)
            probe_end = int(probe[2]) + desired_spaces
    return filtered_probes

def get_probe_pairs(sequences, desired_spaces): 
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

def create_pair_metadata(pairs, initiator_name, left_initiator_seq, left_initiator_spacer, 
                         right_initiator_seq, right_initiator_spacer):
    last_seq_end = 0
    pair_metadata = []
    for index in range(0, len(pairs)):
        left = pairs[index][0]
        left_seq_reverse_complement = reverseComplement(left[3])
        right = pairs[index][1]
        right_seq_reverse_complement = reverseComplement(right[3])
        left_space = int(left[1]) - int(last_seq_end)
        right_space = int(right[1]) - int(left[2])
        set_num = index + 1
        left_final_name = left[0] + "_" + str(set_num) + "." + str(1) + "_" + initiator_name
        right_final_name = right[0] + "_" + str(set_num) + "." + str(2) + "_" + initiator_name 
        left_final_probe = left_initiator_seq + left_initiator_spacer + left_seq_reverse_complement
        right_final_probe = right_seq_reverse_complement + right_initiator_spacer + right_initiator_seq
        left_meta = [left_space, set_num, left_seq_reverse_complement, '_' + initiator_name, 
                     left_final_name, left_initiator_seq, left_initiator_spacer, 
                     left_seq_reverse_complement, left_final_probe]
        right_meta = [right_space, set_num, right_seq_reverse_complement, '_' + initiator_name, 
                      right_final_name, right_seq_reverse_complement, right_initiator_spacer, 
                      right_initiator_seq, right_final_probe]
        pair_metadata.append([left_meta, right_meta])
        last_seq_end = right[2]
    return pair_metadata

def append_metadata_to_probes(probes, metadata):
    i = 0
    probes_with_meta = []
    while i < len(probes) and i < len(metadata):
        first = probes[i][0] + metadata[i][0]
        second = probes[i][1] + metadata[i][1]
        probes_with_meta.append([first, second])
        i += 1
    return probes_with_meta

def main():
    userInput = ArgumentParser(description="Requires a path to a bed file from which to read probes. Takes an integer value to determine "
                                            + "the number of spaces between probes in a pair. Also takes initiator sequences and an initiator spacer "
                                            + "for appending to the probes. Outputs a csv containing candidate probe pairs.")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-p', '--Path', action='store', required=True,
                                help='The bed file with probe sequences')
    requiredNamed.add_argument('-s', '--Spaces', action='store', required=True,
                                help="Desired number of spaces between probes in a pair")
    requiredNamed.add_argument('-i', '--Initiator', action='store', required=True,
                                help="The initiator name")
    requiredNamed.add_argument('-l', '--LeftSeq', action='store', required=True,
                                help="The left initiator sequence")
    requiredNamed.add_argument('--LeftSpacer', action='store', required=True,
                                help="The left initiator spacer")   
    requiredNamed.add_argument('-r', '--RightSeq', action='store', required=True,
                                help="The right initiator sequence")
    requiredNamed.add_argument('--RightSpacer', action='store', required=True,
                                help="The right initiator spacer")
    args = userInput.parse_args()
    input_path = args.Path
    desired_spaces = int(args.Spaces)
    initiator_name = args.Initiator
    left_initiator_seq = args.LeftSeq
    left_initiator_spacer = args.LeftSpacer
    right_initiator_seq = args.RightSeq
    right_initiator_spacer = args.RightSpacer

    candidate_probes = read_probes(input_path)
    filtered_probes = filter_probes_by_spaces(candidate_probes, desired_spaces)
    pairs = get_probe_pairs(filtered_probes, desired_spaces)
    pair_meta = create_pair_metadata(pairs, initiator_name, left_initiator_seq, left_initiator_spacer, 
                                     right_initiator_seq, right_initiator_spacer)
    pairs_with_meta = append_metadata_to_probes(pairs, pair_meta)
    
    probeWriter.write_probes_with_metadata(pairs_with_meta)
    probeWriter.write_probes_for_alignment_fasta(pairs, desired_spaces)
    probeWriter.write_probes_to_csv(pairs_with_meta)

    #TODO Filtering of block parse probes is arbitrary. Consider strategy to optimize 

if __name__ == '__main__':
    main()
