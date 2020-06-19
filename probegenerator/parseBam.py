from __future__ import print_function
from argparse import ArgumentParser
from pysam import AlignmentFile
from utils.initiator_utils import parse_initiators
from utils.file_writer_utils import write_specific_probes
import constants
import os
import csv
import re

def parse_alignment_bam(file_path):
    '''
    Parse bam or sam file with pysam.
    '''
    bamfile = AlignmentFile(file_path, 'rb', check_header=False, check_sq=False)
    return [read for read in bamfile.fetch()]

def filter_reads_by_alignment_qual(reads):
    '''
    Filters all reads that do not have exactly one alignment. Also filter
    reads that have an alignment score less than -10. Assumes bowtie2 end-to-end mode.
    '''
    filtered_reads = []
    for read in reads:
        if not read.has_tag('AS'):
            continue
        if read.has_tag('XS'):
            continue
        if read.get_tag('AS') >= -10:
            filtered_reads.append(read)
    return filtered_reads

def retrieve_specific_probes_from_csv(csv_path, specific_probes):
    '''
    Extract specific probes from the csv file output by the probeGenerator script.
    '''
    good_sets = [re.sub('[^0-9]', '', probe.query_name) for probe in specific_probes]
    with open(csv_path) as probes:
        good_probes = []
        reader = csv.DictReader(probes)
        for row in reader:
            if row['set'] in good_sets:
                good_probes.append(row)
        return good_probes

def get_final_probes(probes):
    '''
    Get all probe pairs that pass the specificity tests. 
    '''
    orf_probes = filter_pairs(probes, pair_in_orf)
    three_utr_probes = filter_pairs(probes, pair_in_three_utr, (get_final_orf_index(probes)))
    five_utr_probes = filter_pairs(probes, pair_in_five_utr, get_final_orf_index(probes))
    return three_utr_probes, five_utr_probes, orf_probes

def filter_pairs(probes, pair_filter, *extra_filter_args):
    '''
    Filters probe pairs based on arbitrary criteria. Expects a boolean function pair_filter
    and optional extra_filter_args to pass to the pair_filter function.
    '''
    filtered_pairs = []
    for i in range(0, len(probes), 2):
        pair = [probes[i], probes[i+1]]
        result = None 
        if extra_filter_args:
            result = pair_filter(pair, *extra_filter_args)
        else:
            result = pair_filter(pair)
        if result:
            filtered_pairs.extend(pair)
    return filtered_pairs        

def num_pairs_in_orf(probes):
    '''
    Determine the number of probe pairs that are in the open reading frame.
    '''
    num_pairs = 0
    for i in range(0, len(probes), 2):
        if pair_in_orf([probes[i], probes[i+1]]):
            num_pairs += 1
    return num_pairs

def get_final_orf_index(probes):
    '''
    Determine the probe with the maximum starting index that is still in the
    open reading frame. 
    '''
    max_orf_index = 0
    for probe in probes:
        if probe['In Orf?'] == 'True' and int(probe['start']) > max_orf_index:
            max_orf_index = int(probe['start'])
    return max_orf_index

def pair_in_orf(pair):
    '''
    Return true if a probe is in the open reading frame.
    '''
    return pair[0]['In Orf?'] == 'True' and pair[1]['In Orf?'] == 'True'

def pair_in_three_utr(pair, final_orf_index):
    '''
    Return true if a probe is in the three prime utr.
    '''
    return int(pair[0]['start']) > final_orf_index or int(pair[1]['start']) > final_orf_index

def pair_in_five_utr(pair, final_orf_index):
    '''
    Return true if a probe is in the five prime utr.
    '''
    return not (pair_in_three_utr(pair, final_orf_index) or pair_in_orf(pair))

def main():
    '''
    Parses the csv files output from the probeGenerator script and the bam files output from bowtie2 to extract 
    specific probe pairs. Writes fasta files containing the extracted probe pairs for the genes in each initiator
    directory. Assumes that output and initiator and gene directories have already been created. 
    '''
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
        good_probes = retrieve_specific_probes_from_csv(os.path.join(constants.OUTPUT_BASE_DIR, initiator[0], input_path), filtered)
        three_utr_probes, five_utr_probes, orf_probes = get_final_probes(good_probes)

        three_name = three_utr_probes[0]['gene name'].split(" ")[0]
        write_specific_probes(os.path.join(constants.OUTPUT_BASE_DIR, initiator[0]), three_name, three_utr_probes, initiator[0])

        five_name = five_utr_probes[0]['gene name'].split(" ")[0]
        write_specific_probes(os.path.join(constants.OUTPUT_BASE_DIR, initiator[0]), five_name, five_utr_probes, initiator[0])

        orf_name = orf_probes[0]['gene name'].split(" ")[0]
        write_specific_probes(os.path.join(constants.OUTPUT_BASE_DIR, initiator[0]), orf_name, orf_probes, initiator[0])

if __name__ == '__main__':
    main()