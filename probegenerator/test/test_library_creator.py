import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import unittest
from probegenerator import library_creator

class TestLibraryCreator(unittest.TestCase):

    def test_get_primer_sequence_empty_data(self):
        primer_data = []
        primer_id = ''

        expected_value = None

        actual_value = library_creator.get_primer_sequence(primer_data, primer_id)
        self.assertEqual(expected_value, actual_value)

    def test_get_primer_sequence_primer_found(self):
        primer_one = {
            'plate_position': 'A1',
            'sequence': 'ATG'
        }
        primer_two = {
            'plate_position': 'D1',
            'sequence': 'GTA'
        }
        primer_data = [primer_one, primer_two]
        primer_id = 'A1'

        expected_value = 'ATG'

        actual_value = library_creator.get_primer_sequence(primer_data, primer_id)
        self.assertEqual(expected_value, actual_value)

    def test_get_primer_sequence_primer_not_found(self):
        primer_one = {
            'plate_position': 'A1',
            'sequence': 'ATG'
        }
        primer_two = {
            'plate_position': 'D1',
            'sequence': 'GTA'
        }
        primer_data = [primer_one, primer_two]
        primer_id = 'G2'

        expected_value = None

        actual_value = library_creator.get_primer_sequence(primer_data, primer_id)
        self.assertEqual(expected_value, actual_value)

    def test_attach_primers_empty_sequences(self):
        sequences = []
        nt_primer = 'AAA'
        nb_primer = 'GGG'
        header_line = True

        expected_value = []

        actual_value = library_creator.attach_primers(sequences, nt_primer, nb_primer, header_line)
        self.assertEqual(expected_value, actual_value)

    def test_attach_primers_header_true(self):
        sequences = ['header', 'TTT', 'CCC']
        nt_primer = 'AAA'
        nb_primer = 'GGG'
        header_line = True

        expected_value = ['AAATTTGGG', 'AAACCCGGG']

        actual_value = library_creator.attach_primers(sequences, nt_primer, nb_primer, header_line)
        self.assertEqual(expected_value, actual_value)

    def test_attach_primers_header_false(self):
        sequences = ['TTT', 'CCC']
        nt_primer = 'AAA'
        nb_primer = 'GGG'
        header_line = False

        expected_value = ['AAATTTGGG', 'AAACCCGGG']

        actual_value = library_creator.attach_primers(sequences, nt_primer, nb_primer, header_line)
        self.assertEqual(expected_value, actual_value)

    def test_strip_fasta_headers_empty_sequences(self):
        sequences = []

        expected_value = []

        actual_value = library_creator.strip_fasta_headers(sequences)
        self.assertEqual(expected_value, actual_value)

    def test_strip_fasta_headers_no_headers(self):
        sequences = ['TTT', 'AAA', 'CCC']

        expected_value = ['TTT', 'AAA', 'CCC']

        actual_value = library_creator.strip_fasta_headers(sequences)
        self.assertEqual(expected_value, actual_value)

    def test_strip_fasta_headers_headers_present(self):
        sequences = ['>AGATAG', 'AAA', '>GGTTA']

        expected_value = ['AAA']

        actual_value = library_creator.strip_fasta_headers(sequences)
        self.assertEqual(expected_value, actual_value)

    def test_get_file_path_without_extension_empty_path(self):
        path = ''

        with self.assertRaises(Exception):
            library_creator.get_file_path_without_extension(path)

    #TODO Failing in build. Fix this
    # def test_get_file_path_without_extension_path_exists(self):
    #     path = os.path.join('probegenerator', 'test', 'test_library_creator.py')

    #     expected_value = 'probegenerator/test/test_library_creator'

    #     actual_value = library_creator.get_file_path_without_extension(path)
    #     self.assertEqual(expected_value, actual_value)   

if __name__ == '__main__':
    unittest.main()