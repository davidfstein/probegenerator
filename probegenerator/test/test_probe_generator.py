import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import unittest
from probegenerator import probeGenerator

class TestProbeGenerator(unittest.TestCase):

    def test_filter_probes_by_spaces_empty_probes(self):
        probes = []
        desired_spaces = 0

        expected_value = []

        actual_value = probeGenerator.filter_probes_by_spaces(probes, desired_spaces)
        self.assertEqual(expected_value, actual_value)

    def test_filter_probes_by_spaces_one(self):
        probe_one = ['gene', 0, 25]
        probe_two = ['gene', 20, 45]
        probes = [probe_one, probe_two]
        desired_spaces = 3

        expected_value = [probe_one]

        actual_value = probeGenerator.filter_probes_by_spaces(probes, desired_spaces)
        self.assertEqual(expected_value, actual_value)

    def test_filter_probes_by_spaces_all(self):
        probe_one = ['gene', 0, 25]
        probe_two = ['gene', 28, 45]
        probes = [probe_one, probe_two]
        desired_spaces = 3

        expected_value = [probe_one, probe_two]

        actual_value = probeGenerator.filter_probes_by_spaces(probes, desired_spaces)
        self.assertEqual(expected_value, actual_value)

    def test_get_probe_pairs_empty(self):
        probes = []
        desired_spaces = 3

        with self.assertRaises(Exception):
            probeGenerator.get_probe_pairs(probes, desired_spaces)

    def test_get_probe_pairs_no_pairs(self):
        probe_one = ['gene', 0, 25]
        probe_two = ['gene', 26, 45]
        probes = [probe_one, probe_two]
        desired_spaces = 3

        expected_value = []

        actual_value = probeGenerator.get_probe_pairs(probes, desired_spaces)
        self.assertEqual(expected_value, actual_value)

    def test_get_probe_pairs_one_pairs(self):
        probe_one = ['gene', 0, 25]
        probe_two = ['gene', 28, 45]
        probes = [probe_one, probe_two]
        desired_spaces = 3

        expected_value = [[probe_one, probe_two]]

        actual_value = probeGenerator.get_probe_pairs(probes, desired_spaces)
        self.assertEqual(expected_value, actual_value)

    def test_get_probe_pairs_prefiltered(self):
        probe_one = ['gene', 0, 25]
        probe_two = ['gene', 26, 43]
        probe_three = ['gene', 28, 45]
        probes = [probe_one, probe_two, probe_three]
        desired_spaces = 3

        expected_value = []

        actual_value = probeGenerator.get_probe_pairs(probes, desired_spaces)
        self.assertEqual(expected_value, actual_value)

    def test_get_probe_pairs_one_in_one_out(self):
        probe_one = ['gene', 0, 25]
        probe_two = ['gene', 26, 43]
        probe_three = ['gene', 46, 69]
        probe_four = ['gene', 72, 90]
        probes = [probe_one, probe_two, probe_three, probe_four]
        desired_spaces = 3

        expected_value = [[probe_two, probe_three]]

        actual_value = probeGenerator.get_probe_pairs(probes, desired_spaces)
        self.assertEqual(expected_value, actual_value)

    def test_append_metadata_to_probes_empty(self):
        probes = []
        metadata = []

        expected_value = []

        actual_value = probeGenerator.append_metadata_to_probes(probes, metadata)
        self.assertEqual(expected_value, actual_value)

    def test_append_metadata_to_probes_mismatch_length(self):
        probes = [0]
        metadata = []

        with self.assertRaises(Exception):
            probeGenerator.append_metadata_to_probes(probes, metadata)

    def test_append_metadata_to_probes_one_pair(self):
        probe_one = ['gene one']
        probe_two = ['gene two']
        metadata_one = ['metadata one']
        metadata_two = ['metadata two']
        pair = [probe_one, probe_two]
        metadatum = [metadata_one, metadata_two]
        probes = [pair]
        metadata = [metadatum]

        probe_one_with_meta = probe_one + metadata_one
        probe_two_with_meta = probe_two + metadata_two
        expected_value = [[probe_one_with_meta, probe_two_with_meta]]

        actual_value = probeGenerator.append_metadata_to_probes(probes, metadata)
        self.assertEqual(expected_value, actual_value)

    def test_is_probe_in_orf_not_in(self):
        probe_start = 0
        probe_length = 25
        orf_start = 30
        orf_length = 100

        self.assertFalse(probeGenerator.is_probe_in_orf(probe_start, probe_length, orf_start, orf_length))

    def test_is_probe_in_orf_part_in(self):
        probe_start = 80
        probe_length = 25
        orf_start = 30
        orf_length = 70

        self.assertFalse(probeGenerator.is_probe_in_orf(probe_start, probe_length, orf_start, orf_length))

    def test_is_probe_in_orf_in(self):
        probe_start = 60
        probe_length = 25
        orf_start = 30
        orf_length = 70

        self.assertTrue(probeGenerator.is_probe_in_orf(probe_start, probe_length, orf_start, orf_length))

    def test_split_on_tabs_empty(self):
        probes = []

        expected_value = []

        actual_value = probeGenerator.split_on_tabs(probes)
        self.assertEqual(expected_value, actual_value)

    def test_split_on_tabs_empty_split(self):
        probes = ['']

        expected_value = []

        actual_value = probeGenerator.split_on_tabs(probes)
        self.assertEqual(expected_value, actual_value)

    def test_split_on_tabs_no_tabs(self):
        probes = ['Hello there.']

        expected_value = [['Hello there.']]

        actual_value = probeGenerator.split_on_tabs(probes)
        self.assertEqual(expected_value, actual_value)

    def test_split_on_tabs_one_tab(self):
        probes = ['Hello\t there.']

        expected_value = [['Hello', ' there.']]

        actual_value = probeGenerator.split_on_tabs(probes)
        self.assertEqual(expected_value, actual_value)

if __name__ == '__main__':
    unittest.main()