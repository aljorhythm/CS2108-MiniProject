import unittest
from midi_properties import MidiProperties
from midi_properties import KeyUtils

import os


class TestMidiProperties(unittest.TestCase):

    def test_get_absolute_pitch(self):
        pairs = [
          [24, 0],
          [25, 1],
          [60, 0],
          [69, 9],
          [95, 11]
        ]
        for pair in pairs:
          midi_note = pair[0]
          absolute_number = pair[1]
          self.assertEqual(KeyUtils.get_absolute_pitch(midi_note), absolute_number)

    def test_get_standard_key(self):
        self.assertEqual(KeyUtils.get_standard_key('Am'), 'C')
        self.assertEqual(KeyUtils.get_standard_key('Bm'), 'D')
        self.assertEqual(KeyUtils.get_standard_key('Cm'), 'D#')
        self.assertEqual(KeyUtils.get_standard_key('Dm'), 'F')
        self.assertEqual(KeyUtils.get_standard_key('Em'), 'G')
        self.assertEqual(KeyUtils.get_standard_key('Eb'), 'D#')
        self.assertEqual(KeyUtils.get_standard_key('Eb'), 'D#')

    def test_are_keys_equal(self):
        equal_keypairs = [
          ['Am', 'C'],
          ['Bm', 'D'],
          ['Cm', 'Eb'],
          ['Eb', 'Eb'],
          ['Dm', 'F'],
          ['Em', 'G']
        ]

        for keypair in equal_keypairs:
          self.assertTrue(KeyUtils.are_keys_equal(keypair[0], keypair[1]), "{} != {}".format(keypair[0], keypair[1]))          

if __name__ == '__main__':
    unittest.main()
