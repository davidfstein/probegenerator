from argparse import ArgumentParser

def find_longest_orf(sequence, start_codon_indices):
    '''
    Finds the longest open reading frame in a given sequence.
    Returns the starting index of the longest open reading frame and
    the length of the lognest open reading frame.
    '''
    best_start_index = 0
    longest_orf_so_far = 0
    for index in start_codon_indices:
        for i in range(0, len(sequence) - index, 3):
            if is_stop_codon(sequence[index+i:index+i+3]):
                current_orf_length = i
                if current_orf_length > longest_orf_so_far:
                    longest_orf_so_far = current_orf_length
                    best_start_index = index
                break
    return (best_start_index + 1, longest_orf_so_far)

def find_start_codons(sequence):
    '''
    Get the indices of all the start codons in the sequence.
    '''
    start_codon_indices = []
    for i in range(len(sequence) - 3):
        if sequence[i:i+3].lower() == 'atg':
            start_codon_indices.append(i)
    return start_codon_indices

def is_stop_codon(sequence):
    '''
    Returns true if the sequence is a stop codon.
    '''
    return sequence.lower() in ['tag', 'taa', 'tga']

def main():
    '''
    Parses a file containing a sequence in the FASTA format. Returns the start index and length
    of the longest open reading frame in the sequence if any exists.
    '''
    userInput = ArgumentParser()
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-p', '--Path', action='store', required=True)
    args = userInput.parse_args()
    path = args.Path

    with open(path) as seq_file:
        lines = seq_file.readlines()
        lines = [line.strip('\n') for line in lines]
        sequence = ''
        for line in lines:
            sequence += line
        start_codon_indices = find_start_codons(sequence)
        start_index, length = find_longest_orf(sequence, start_codon_indices)
        return start_index, length

if __name__ == '__main__':
    main()