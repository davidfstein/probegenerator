import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import unittest
import pysam
from probegenerator import parseBam

class TestParseBam(unittest.TestCase):

    def test_pair_in_orf_both_in(self):
        probe_one = {'In Orf?': "True"}
        probe_two = {'In Orf?': "True"}
        pair = [probe_one, probe_two]
        self.assertTrue(parseBam.pair_in_orf(pair))

    def test_pair_in_orf_one_in_one_out(self):
        probe_one = {'In Orf?': "False"}
        probe_two = {'In Orf?': "True"}
        pair = [probe_one, probe_two]
        self.assertFalse(parseBam.pair_in_orf(pair))

    def test_pair_in_orf_both_out(self):
        probe_one = {'In Orf?': "False"}
        probe_two = {'In Orf?': "False"}
        pair = [probe_one, probe_two]
        self.assertFalse(parseBam.pair_in_orf(pair))

    def test_pair_in_three_prime_both_in(self):
        final_orf_index = 5
        probe_one = {'start': 10}
        probe_two = {'start': 35}
        pair = [probe_one, probe_two]
        self.assertTrue(parseBam.pair_in_three_utr(pair, final_orf_index))
        
    def test_pair_in_three_prime_one_in(self):
        final_orf_index = 15
        probe_one = {'start': 10}
        probe_two = {'start': 35}
        pair = [probe_one, probe_two]
        self.assertTrue(parseBam.pair_in_three_utr(pair, final_orf_index))

    def test_pair_in_three_prime_both_out(self):
        final_orf_index = 45
        probe_one = {'start': 10}
        probe_two = {'start': 35}
        pair = [probe_one, probe_two]
        self.assertFalse(parseBam.pair_in_three_utr(pair, final_orf_index))

    def test_pair_in_three_prime_first_equal(self):
        final_orf_index = 10
        probe_one = {'start': 10}
        probe_two = {'start': 35}
        pair = [probe_one, probe_two]
        self.assertTrue(parseBam.pair_in_three_utr(pair, final_orf_index))

    def test_pair_in_three_prime_second_equal(self):
        final_orf_index = 35
        probe_one = {'start': 10}
        probe_two = {'start': 35}
        pair = [probe_one, probe_two]
        self.assertFalse(parseBam.pair_in_three_utr(pair, final_orf_index))

    def test_get_final_orf_index(self):
        probe_one ={
            'start': 10,
            'In Orf?': 'True'
        }
        probe_two ={
            'start': 20,
            'In Orf?': 'True'
        }
        self.assertEqual(parseBam.get_final_orf_index([probe_one, probe_two]), 20)

    def test_num_pairs_in_orf(self):
        self.assertEqual(parseBam.num_pairs_in_orf([]), 0)

    def test_num_pairs_in_orf_both_in(self):
        probe_one = {'In Orf?': "True"}
        probe_two = {'In Orf?': "True"}
        self.assertEqual(parseBam.num_pairs_in_orf([probe_one, probe_two]), 1)

    def test_num_pairs_in_orf_one_in_one_out(self):
        probe_one = {'In Orf?': "True"}
        probe_two = {'In Orf?': "False"}
        self.assertEqual(parseBam.num_pairs_in_orf([probe_one, probe_two]), 0)

    def test_pair_filter_empty(self):
        test_filter = lambda x: x == 0
        self.assertEqual(parseBam.filter_pairs([], test_filter), [])

    def test_pair_filter_one_match(self):
        test_filter = lambda pair: pair[0] == 5 and pair[1] == 6
        probes = [5, 6, 7, 8]
        self.assertEqual(parseBam.filter_pairs(probes, test_filter), [5, 6])

    def test_get_final_probes_all_in_orf(self):
        desired_number = 4
        probe_one = {
            'start': 0,
            'In Orf?': 'True'
        }
        probe_two = {
            'start': 28,
            'In Orf?': 'True'
        }
        probe_three = {
            'start': 50,
            'In Orf?': 'True'
        }
        probe_four = {
            'start': 78,
            'In Orf?': 'True'
        }
        probe_five = {
            'start': 200,
            'In Orf?': 'False'
        }
        probe_six = {
            'start': 228,
            'In Orf?': 'False'
        }
        probes = [probe_one, probe_two, probe_three, probe_four, probe_five, probe_six]
        final_probes = [probe_one, probe_two, probe_three, probe_four]
        self.assertEqual(parseBam.get_final_probes(probes, desired_number), final_probes)

    def test_get_final_probes_two_orf_two_three_prime(self):
        desired_number = 4
        probe_one = {
            'start': 0,
            'In Orf?': 'False'
        }
        probe_two = {
            'start': 28,
            'In Orf?': 'False'
        }
        probe_three = {
            'start': 50,
            'In Orf?': 'True'
        }
        probe_four = {
            'start': 78,
            'In Orf?': 'True'
        }
        probe_five = {
            'start': 200,
            'In Orf?': 'False'
        }
        probe_six = {
            'start': 228,
            'In Orf?': 'False'
        }
        probes = [probe_one, probe_two, probe_three, probe_four, probe_five, probe_six]
        final_probes = [probe_three, probe_four, probe_five, probe_six]
        self.assertEqual(parseBam.get_final_probes(probes, desired_number), final_probes)

    def test_get_final_probes_take_all(self):
        desired_number = 6
        probe_one = {
            'start': 0,
            'In Orf?': 'False'
        }
        probe_two = {
            'start': 28,
            'In Orf?': 'False'
        }
        probe_three = {
            'start': 50,
            'In Orf?': 'True'
        }
        probe_four = {
            'start': 78,
            'In Orf?': 'True'
        }
        probe_five = {
            'start': 200,
            'In Orf?': 'False'
        }
        probe_six = {
            'start': 228,
            'In Orf?': 'False'
        }
        probes = [probe_one, probe_two, probe_three, probe_four, probe_five, probe_six]
        final_probes = [probe_three, probe_four, probe_five, probe_six, probe_one, probe_two]
        self.assertEqual(parseBam.get_final_probes(probes, desired_number), final_probes)

    def test_filter_reads_by_alignment_qual_empty(self):
        reads = []
        self.assertEqual(parseBam.filter_reads_by_alignment_qual([]), [])

    def test_filter_reads_by_alignment_qual_none_specific(self):
        read_one = pysam.AlignedSegment()
        read_one.set_tag('AS', 0)
        read_one.set_tag('XS', 0)
        reads = [read_one]
        self.assertEqual(parseBam.filter_reads_by_alignment_qual(reads), [])

    def test_filter_reads_by_alignment_qual_one_specific(self):
        read_one = pysam.AlignedSegment()
        read_one.set_tag('AS', 0)
        read_one.set_tag('XS', 0)
        read_two = pysam.AlignedSegment()
        read_two.set_tag('AS', 0)
        reads = [read_one, read_two]
        self.assertEqual(parseBam.filter_reads_by_alignment_qual(reads), [read_two])

    def test_filter_reads_by_alignment_qual_low_specificity(self):
        read_one = pysam.AlignedSegment()
        read_one.set_tag('AS', -11)
        reads = [read_one]
        self.assertEqual(parseBam.filter_reads_by_alignment_qual(reads), [])

    def test_filter_reads_by_alignment_qual_no_alignment(self):
        read_one = pysam.AlignedSegment()
        reads = [read_one]
        self.assertEqual(parseBam.filter_reads_by_alignment_qual(reads), [])

if __name__ == '__main__':
    unittest.main()