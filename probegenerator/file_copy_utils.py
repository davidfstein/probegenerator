from __future__ import print_function
from shutil import copyfile
from argparse import ArgumentParser
import csv
import os

def main():
    userInput = ArgumentParser(description="")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-i', '--Initiators', action='store', required=True)
    requiredNamed.add_argument('-n', '--Name', action='store', required=True)

    args = userInput.parse_args()
    initiator_file = args.Initiators
    copy_file_name = args.Name

    initiators = []
    with open(initiator_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            initiators.append([ row['initiator'], row['left sequence'], row['left spacer'], row['right sequence'], row['right spacer'] ]) 
    
    for initiator in initiators:
        copyfile(copy_file_name + '.bam', os.path.join('/data', 'output', initiator[0], copy_file_name, copy_file_name + '.bam'))

if __name__ == '__main__':
    main()