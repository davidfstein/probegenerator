from __future__ import print_function
from reverseComplement import reverseComplement
from argparse import ArgumentParser
import csv

def write_probes_to_csv(pairs, pair_meta, tags):
    with open('./' + 'test' + '_probes.csv', 'w+') as probes:
        writer = csv.writer(probes, delimiter=",")
        writer.writerow(['gene name', 'start', 'stop', 'seq', 'tm', 'spacing', 'set', 'probe', 'amplifier', 'final name', 'left', 'spacer', 'right', 'final probe', 'alignment score', 'off-target score'])
        write_body(writer, pairs, pair_meta, tags)

def write_body(writer, pairs, pair_meta, tags):
    for i in range(0, len(tags)):
        writer.writerow(pair_meta[i] + tags[i])
        writer.writerow(pair_meta[i+1] + tags[i])

def main():
    userInput = ArgumentParser(description="")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('--TagFile', action='store', required=True)
    requiredNamed.add_argument('-p', '--Probes', action='store', required=True)

    args = userInput.parse_args()
    tags = args.TagFile
    probes = args.Probes

    parsed_tags = []
    with open(tags) as tag_file:
        for tag in tag_file:
            tag = tag.strip('\n')
            tag = tag.split(',')
            parsed_tags.append(tag)

    parsed_probes = []
    with open(probes) as probe_file:
        for probe in probe_file:
            probe = probe.strip("[]\n")
            probe = probe.split(',')
            parsed_probes.append(probe)

    write_probes_to_csv([], parsed_probes, parsed_tags)

if __name__ == '__main__':
    main()