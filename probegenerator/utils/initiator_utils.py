import csv

def parse_initiators(initiator_file):
    '''
    Parse a csv with initiators into a list.
    '''
    initiators = []
    with open(initiator_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            initiators.append([ row['initiator'], row['left sequence'], row['left spacer'], row['right sequence'], row['right spacer'] ])
    return initiators