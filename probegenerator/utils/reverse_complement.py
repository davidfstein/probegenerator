
def reverseComplement(sequence):
    reverseSequence = reverseString(sequence)
    return getComplement(reverseSequence)

def reverseString(string):
    return string[::-1]

def getComplement(sequence):
    complements = {"A": "T", "T": "A", "G": "C", "C": "G"}
    return ''.join([complements[nuc] for nuc in list(sequence)])