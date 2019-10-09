import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import unittest
from probegenerator import orf_finder

class TestParseBam(unittest.TestCase):

    def test_find_longest_orf_one_orf(self):
        sequence = 'AAAAUGTACGACTAGCTT'
        start_indices = [3]

        expected_longest_orf_length = 9
        expected_best_start_index = 3
        
        actual_best_index, actual_longest_orf_length = orf_finder.find_longest_orf(sequence, start_indices)
        self.assertEqual( (actual_best_index, actual_longest_orf_length), 
                          (expected_best_start_index, expected_longest_orf_length) )

    def test_find_longest_orf_no_stop(self):
        sequence = 'AAAATGTACGACAAGCTT'
        start_indices = [3]

        expected_longest_orf_length = 0
        expected_best_start_index = 0
        
        actual_best_index, actual_longest_orf_length = orf_finder.find_longest_orf(sequence, start_indices)
        self.assertEqual( (actual_best_index, actual_longest_orf_length), 
                          (expected_best_start_index, expected_longest_orf_length) )

    def test_find_longest_orf_no_start(self):
        sequence = 'AAAATGTACGACAAGCTT'
        start_indices = []

        expected_longest_orf_length = 0
        expected_best_start_index = 0
        
        actual_best_index, actual_longest_orf_length = orf_finder.find_longest_orf(sequence, start_indices)
        self.assertEqual( (actual_best_index, actual_longest_orf_length), 
                          (expected_best_start_index, expected_longest_orf_length) )

    def test_find_longest_orf_two_orfs(self):
        sequence = 'ATGCCCTAAAAAATGTACGACTAGCTT'
        start_indices = [0, 12]

        expected_longest_orf_length = 9
        expected_best_start_index = 12
        
        actual_best_index, actual_longest_orf_length = orf_finder.find_longest_orf(sequence, start_indices)
        self.assertEqual( (actual_best_index, actual_longest_orf_length), 
                          (expected_best_start_index, expected_longest_orf_length) )

    def test_find_start_codons_none(self):
        sequence = 'AAGCCCTAAAAAAAGTACGACTAGCTT'

        expected_indices = []

        actual_indices = orf_finder.find_start_codons(sequence)
        self.assertEqual(actual_indices, expected_indices)

    def test_find_start_codons_empty_sequence(self):
        sequence = ''

        expected_indices = []

        actual_indices = orf_finder.find_start_codons(sequence)
        self.assertEqual(actual_indices, expected_indices)

    def test_find_start_codons_one(self):
        sequence = 'AAGCCCTAAAAAATGTACGACTAGCTT'

        expected_indices = [12]

        actual_indices = orf_finder.find_start_codons(sequence)
        self.assertEqual(actual_indices, expected_indices)
    
    def test_find_start_codons_two(self):
        sequence = 'ATGCCCTAAAAAATGTACGACTAGCTT'

        expected_indices = [0, 12]

        actual_indices = orf_finder.find_start_codons(sequence)
        self.assertEqual(actual_indices, expected_indices)

    def test_is_stop_codon_empty_sequence(self):
        sequence = ''

        actual = orf_finder.is_stop_codon(sequence)
        self.assertFalse(actual)

    def test_is_stop_codon_long_sequence(self):
        sequence = 'TAGTAA'

        actual = orf_finder.is_stop_codon(sequence)
        self.assertFalse(actual)

    def test_is_stop_codon_stop_sequence(self):
        sequence = 'TAA'

        actual = orf_finder.is_stop_codon(sequence)
        self.assertTrue(actual)

if __name__ == '__main__':
    unittest.main()