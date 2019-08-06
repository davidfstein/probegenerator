from argparse import ArgumentParser

def find_longest_orf(sequence, start_codon_indices):
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
    start_codon_indices = []
    for i in range(len(sequence) - 3):
        if sequence[i:i+3].lower() == 'atg':
            start_codon_indices.append(i)
    return start_codon_indices

def is_stop_codon(sequence):
    return sequence.lower() in ['tag', 'taa', 'tga']

def reverse_complement(sequence):
    reverseSequence = reverseString(sequence)
    return getComplement(reverseSequence)

def reverseString(string):
    return string[::-1]

def getComplement(sequence):
    complements = {"A": "T", "T": "A", "G": "C", "C": "G"}
    return ''.join([complements[nuc] for nuc in list(sequence)])

def main():
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