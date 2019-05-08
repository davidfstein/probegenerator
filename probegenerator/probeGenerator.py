from argparse import ArgumentParser
from reverseComplement import reverseComplement
import sys
import csv

def getProbePairs(input_path, desired_spaces, initiator_name, left_initiator_seq, left_initiator_spacer, 
                    right_initiator_seq, right_initiator_spacer):
    seqf=[]
    probeend = 0
    with open (input_path) as gene:
        seq = [line.rstrip("\n").split("\t") for line in gene if len(line.rstrip("\n").split("\t")) > 0]
        for seqn in seq:
            if int(seqn[1]) >= probeend:
                seqf.append(seqn)
                probeend = (int(seqn[2]) + int(desired_spaces))
    pairs = create_pairs(seqf)
    write_probes_to_csv(pairs, desired_spaces, initiator_name, left_initiator_seq, left_initiator_spacer, right_initiator_seq, right_initiator_spacer)

def create_pairs(sequences): 
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
        if (cur_start - prev_end == 3):
            pairs.append([previous_sequence, sequence])
        previous_sequence = sequence    

    return pairs

def write_probes_to_csv(seq_pairs, desired_spaces, initiator_name, left_initiator_seq, left_initiator_spacer, right_initiator_seq, right_initiator_spacer):
    with open('./' + seq_pairs[0][0][0] + '_probes.csv', 'w+') as probes:
        writer = csv.writer(probes, delimiter=",")
        writer.writerow(['gene name', 'start', 'stop', 'seq', 'tm', 'spacing', 'set', 'probe', 'amplifier', 'final name', 'left', 'spacer', 'right', 'final probe'])
        write_body(writer, seq_pairs, initiator_name, left_initiator_seq, left_initiator_spacer, right_initiator_seq, right_initiator_spacer)

def write_body(writer, pairs, initiator_name, left_initiator_seq, left_initiator_spacer, right_initiator_seq, right_initiator_spacer):
    last_seq_end = 0
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
        writer.writerow([left[0], 
                        left[1], 
                        left[2], 
                        left_seq_reverse_complement, 
                        left[4], 
                        left_space, 
                        set_num, 
                        1, 
                        "_" + initiator_name, 
                        left_final_name, 
                        left_initiator_seq, 
                        left_initiator_spacer, 
                        left_seq_reverse_complement, 
                        left_final_probe])
        writer.writerow([right[0], 
                        right[1], 
                        right[2], 
                        right_seq_reverse_complement, 
                        right[4], 
                        right_space, 
                        set_num, 
                        2, 
                        "_" + initiator_name, 
                        right_final_name, 
                        right_seq_reverse_complement, 
                        right_initiator_spacer, 
                        right_initiator_seq, 
                        right_final_probe])
        last_seq_end = right[2]

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
    desired_spaces = args.Spaces
    initiator_name = args.Initiator
    left_initiator_seq = args.LeftSeq
    left_initiator_spacer = args.LeftSpacer
    right_initiator_seq = args.RightSeq
    right_initiator_spacer = args.RightSpacer
    
    getProbePairs(input_path, desired_spaces, initiator_name, left_initiator_seq, left_initiator_spacer, right_initiator_seq, right_initiator_spacer)

if __name__ == '__main__':
    main()
