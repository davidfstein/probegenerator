from __future__ import print_function
from argparse import ArgumentParser
from pysam import AlignmentFile
from probeGenerator import parse_initiators
import constants
import os
import csv
import re

def parse_alignment_bam(file_path):
    bamfile = AlignmentFile(file_path, 'rb', check_header=False, check_sq=False)
    return [read for read in bamfile.fetch()]

def filter_reads_by_alignment_qual(reads):
    filtered_reads = []
    for read in reads:
        if not read.has_tag('AS'):
            continue
        if read.has_tag('XS'):
            continue
        if read.get_tag('AS') >= -10:
            filtered_reads.append(read)
    return filtered_reads

def remove_non_specific_probes(csv_path, specific_probes):
    good_sets = [re.sub('[^0-9]', '', probe.query_name) for probe in specific_probes]
    with open(csv_path) as probes:
        good_probes = []
        reader = csv.DictReader(probes)
        for row in reader:
            if row['set'] in good_sets:
                good_probes.append(row)
        return good_probes

def get_final_probes(probes):
    final_probes = []
    orf_probes = get_pairs_in_orf(probes)
    if len(orf_probes) >= 100:
        final_probes.extend(orf_probes[0:100])
        return final_probes
    else:
        final_probes.extend(orf_probes)
    three_utr_probes = get_pairs_in_three_utr(probes)
    probes_needed = 100 - len(final_probes)
    if len(three_utr_probes) >= probes_needed:
        final_probes.extend(three_utr_probes[0:probes_needed])
        return final_probes
    else:
        final_probes.extend(three_utr_probes)
    five_utr_probes = get_pairs_in_five_utr(probes)
    probes_needed = 100 - len(final_probes)
    if len(five_utr_probes) >= probes_needed:
        final_probes.extend(five_utr_probes[0:probes_needed])
        return final_probes
    final_probes.extend(five_utr_probes)
    return final_probes

def get_pairs_in_orf(probes):
    orf_probes = []
    for i in range(0, len(probes), 2):
        pair = [probes[i], probes[i+1]]
        if pair_in_orf(pair):
            orf_probes.extend(pair)
    return orf_probes

def get_pairs_in_three_utr(probes):
    three_utr_probes = []
    final_orf_index = get_final_orf_index(probes)
    for i in range(0, len(probes), 2):
        pair = [probes[i], probes[i+1]]
        if pair_in_three_utr(pair, final_orf_index):
            three_utr_probes.extend(pair)
    return three_utr_probes

def get_pairs_in_five_utr(probes):
    five_utr_probes = []
    final_orf_index = get_final_orf_index(probes)
    for i in range(0, len(probes), 2):
        pair = [probes[i], probes[i+1]]
        if not pair_in_orf(pair) and not pair_in_three_utr(pair, final_orf_index):
            five_utr_probes.extend(pair)
    return five_utr_probes

def num_pairs_in_orf(probes):
    num_pairs = 0
    for i in range(0, len(probes), 2):
        if pair_in_orf([probes[i], probes[i+1]]):
            num_pairs += 1
    return num_pairs

def pair_in_orf(pair):
    return pair[0]['In Orf?'] == 'True' and pair[1]['In Orf?'] == 'True'

def get_final_orf_index(probes):
    max_orf_index = 0
    for probe in probes:
        if probe['In Orf?'] == 'True' and int(probe['start']) > max_orf_index:
            max_orf_index = int(probe['start'])
    return max_orf_index

def pair_in_three_utr(pair, final_orf_index):
    return int(pair[0]['start']) > final_orf_index

def write_specific_probes(path, probes, initiator):
    name = probes[0]['gene name'].split(" ")[0]
    with open(os.path.join(path, name, name) + '.fasta', 'w+') as f:
        f.write(">" + name + " probes initiator " + initiator + "\n")
        for i in range(0, len(probes), 2):
            f.write(probes[i]['final probe'] + '\n')
            f.write(probes[i+1]['final probe'] + '\n')

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
    with open('../probe_scores.txt', 'w+') as file:
        for score in scores:
            file.write(str(score) + '\n')

def main():
    userInput = ArgumentParser(description="")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-p', '--Path', action='store', required=True)
    requiredNamed.add_argument('-p2', '--Path2', action='store', required=True)
    requiredNamed.add_argument('-i', '--Initiator', action='store', required=True)
    args = userInput.parse_args()
    input_path = args.Path
    path = args.Path2
    initiator_file = args.Initiator

    initiators = parse_initiators(initiator_file)
    for initiator in initiators:
        reads = parse_alignment_bam(os.path.join(constants.OUTPUT_BASE_DIR, initiator[0], path))
        filtered = filter_reads_by_alignment_qual(reads)
        good_probes = remove_non_specific_probes(os.path.join(constants.OUTPUT_BASE_DIR, initiator[0], input_path), filtered)
        final_probes = get_final_probes(good_probes)
        write_specific_probes(os.path.join(constants.OUTPUT_BASE_DIR, initiator[0]), final_probes, initiator[0])

if __name__ == '__main__':
    main()