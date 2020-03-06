from __future__ import print_function
from reverse_complement import reverseComplement
from argparse import ArgumentParser
from Bio import SeqIO
import csv
import os

def write_probes_for_alignment_fasta(pairs, desired_spaces):
    '''
    Writes probes to disk in the fasta format. Probes are seperated into pairs and
    fasta headers are use the pair set numbers as identifiers.
    '''
    with open('../probes_for_alignment.fa', 'w+') as file:
        for index in range(len(pairs)):
            file.write('>pair' + str(index + 1) + '\n')
            spacer = ''.join(['N' for _ in range(0, int(desired_spaces) - 1)])
            file.write(reverseComplement(pairs[index][1][3]) + spacer + reverseComplement(pairs[index][0][3]) + '\n')

def write_probes_to_csv(pairs, path='.'):
    '''
    Writes probe pairs with metadata to a csv file.
    '''
    name = pairs[0][0][0].split(" ")[0] + '_probes.csv'
    with open(os.path.join(path, name), 'w+') as probes:
        writer = csv.writer(probes, delimiter=",")
        writer.writerow(['gene name', 'start', 'stop', 'seq', 'tm', 'spacing', 'set', 'probe', 'amplifier', 'final name', 'left', 'spacer', 'right', 'final probe', 'In Orf?'])
        write_body(writer, pairs)

def write_body(writer, pairs):
    for pair in pairs:
        writer.writerow(pair[0])
        writer.writerow(pair[1])

def write_specific_probes(path, probes, initiator):
    '''
    Writes probes to disk in the fasta format. Probes grouped by gene and initiator.
    '''
    name = probes[0]['gene name'].split(" ")[0]
    with open(os.path.join(path, name, name) + '.fasta', 'w+') as f:
        f.write(">" + name + " probes initiator " + initiator + "\n")
        for i in range(0, len(probes), 2):
            f.write(probes[i]['final probe'] + '\n')
            f.write(probes[i+1]['final probe'] + '\n')

def write_fasta(records):
    '''
    Write fasta records as individual fasta files on disk. Return the names of the files 
    without the file extenstion.
    '''
    names = []
    for record in records:
        name = '../' + strip_filename_illegal_characters(record.name) + '.fa'
        # OligoMiner breaks if there isn't a newline in a sequence
        newline_sequence = record.seq()
        if len(record.seq.split('\n')[0]) > 25:
            newline_sequence = record.seq()[0:25] + '\n' + record.seq[25:]
        with open(name, 'w+') as f:
            f.write(">" + name + " " + record.description)
            f.write(newline_sequence)
        names.append(name[:-3])
    return names

def strip_filename_illegal_characters(name):
    '''
    Strip some illegal characters from file names. May not be consistent across operating
    systems. 
    '''
    name = name.replace('/', '').replace(':', '').replace('\\', '').replace('.', '').replace('|', '')
    return name

def convert_file_contents_to_list(path, strip_chars='[]\n', split_char=','):
	with open(path) as file:
		return [line.strip(strip_chars).split(split_char) for line in file.readlines()]
