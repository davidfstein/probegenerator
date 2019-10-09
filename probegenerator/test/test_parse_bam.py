import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
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

if __name__ == '__main__':
    unittest.main()