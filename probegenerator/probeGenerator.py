from argparse import parseArgs
from reverseComplement import reverseComplement
import sys
import csv

## TODO : get amplifier as arg
def getProbePairs(input_path, desired_spaces):
    seqf=[]
    probeend = 0
    with open (input_path) as gene:
        seq = [line.rstrip("\n").split("\t") for line in gene if len(line.rstrip("\n").split("\t")) > 0]
        for seqn in seq:
            if int(seqn[1]) >= probeend:
                seqf.append(seqn)
                probeend = (int(seqn[2]) + int(desired_spaces))
    pairs = create_pairs(seqf)
    write_probes_to_csv(pairs, desired_spaces)

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

    # TODO : just pass these as pairs to make write body easier
    return [seq for pair in pairs for seq in pair]


def write_probes_to_csv(seq_pairs, desired_spaces):
    with open('./probes.csv', 'w+') as probes:
        writer = csv.writer(probes, delimiter=",")
        writer.writerow(['SHH', 'start', 'stop', 'seq', 'tm', 'spacing', 'underscore', 'set', 'dot', 'probe', 'amplifier', 'final name', 'left', 'spacer', 'right', 'final probe'])
        write_body(writer, seq_pairs, desired_spaces)

def write_body(writer, seqf, desired_spaces):
    last_index = 0
    set_num = 0
    for i in range(0, len(seqf)):
        line = seqf[i]
        line[3] = reverseComplement(line[3])
        dot = "."
        underscore = "_"
        amplifier = "_B4"
        space = int(line[1]) - int(last_index)
        left = ''
        right = ''
        spacer = ''
        if space >= desired_spaces:
            continue
        if set_num == 0:
            set_num = 1
        if i >= 2 and i % 2 == 0:
            set_num += 1
        ## do this better
        if i == 0:
            probe_num = 1
        else:
            probe_num = (i % 2) + 1
        if probe_num == 1:
            left = 'CCTCAACCTACCTCCAAC'
            spacer = 'AA'
            right = line[3]
        else:
            left = line[3]
            spacer = 'AT'
            right = 'TCTCACCATATTCgCTTC'
        
        last_index = line[2]
        final_name = line[0] + underscore + str(set_num) + dot + str(probe_num) + amplifier
        final_probe = left + spacer + right
        writer.writerow([line[0], line[1], line[2], line[3], line[4], space, underscore, set_num, dot, probe_num, amplifier, final_name, left, spacer, right, final_probe])

if __name__ == '__main__':
    inputPath, desiredSpaces = parseArgs(sys.argv[1:])
    getProbePairs(inputPath, desiredSpaces)
