from __future__ import print_function
from reverseComplement import reverseComplement
from argparse import ArgumentParser
import csv

def write_probes_for_alignment_fasta(pairs, desired_spaces):
    with open('../probes_for_alignment.fa', 'w+') as file:
        for index in range(len(pairs)):
            file.write('>pair' + str(index + 1) + '\n')
            spacer = ''.join(['N' for _ in range(0, int(desired_spaces))])
            file.write(reverseComplement(pairs[index][1][3]) + spacer + reverseComplement(pairs[index][0][3]) + '\n')

def write_probes_with_metadata(probe_metadata):
    with open('../probes_with_meta.txt', 'w+') as file:
        for pair in probe_metadata:
            file.write(str(pair[0]) + '\n')
            file.write(str(pair[1]) + '\n')

def write_probes_to_csv(pairs):
    with open('./' + pairs[0][0][0].split(" ")[0] + '_probes.csv', 'w+') as probes:
        writer = csv.writer(probes, delimiter=",")
        writer.writerow(['gene name', 'start', 'stop', 'seq', 'tm', 'spacing', 'set', 'probe', 'amplifier', 'final name', 'left', 'spacer', 'right', 'final probe', 'In Orf?'])
        write_body(writer, pairs)

def write_body(writer, pairs):
    for pair in pairs:
        writer.writerow(pair[0])
        writer.writerow(pair[1])

def convert_file_contents_to_list(path, strip_chars='[]\n', split_char=','):
	with open(path) as file:
		return [line.strip(strip_chars).split(split_char) for line in file.readlines()]

def main():
    userInput = ArgumentParser(description="")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-p', '--Probes', action='store', required=True)

    args = userInput.parse_args()
    probe_file = args.Probes

    parsed_probes = convert_file_contents_to_list(probe_file)

    write_probes_to_csv(parsed_probes)

if __name__ == '__main__':
    main()