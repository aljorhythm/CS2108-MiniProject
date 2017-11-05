import unittest
from midi_properties import MidiProperties
from midi_properties import KeyUtils

import os


class TestMidiProperties(unittest.TestCase):

    def test_flat_to_sharp(self):
        pairs = [
            ['Ab', 'G#'],
            ['C', 'C'],
            ['C#', 'C#'],
            ['Bb', 'A#'],
            ['Gb', 'F#'],
            ['Eb', 'D#']
        ]

        for pair in pairs:
            self.assertEqual(KeyUtils.flat_to_sharp(pair[0]), pair[1])

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
            converted = KeyUtils.get_absolute_pitch(midi_note)
            self.assertEqual(converted, absolute_number, "MIDI {}, CONVERTED {}, EXPECTED {}".format(
                midi_note, converted, absolute_number))

    def test_get_standard_key(self):
        pairs = [
            ['Am', 'C'],
            ['Bm', 'D'],
            ['Cm', 'D#'],
            ['Eb', 'D#'],
            ['Dm', 'F'],
            ['Em', 'G'],
            ['Eb', 'D#'],
            ['Abm', "B"]
        ]

        for pair in pairs:
            result = KeyUtils.get_standard_key(pair[0])
            self.assertEqual(
                result, pair[1], "Expected {} \t, actual {}".format(pair[1], result))

    def test_are_keys_equal(self):
        equal_keypairs = [
            ['Am', 'C'],
            ['Bm', 'D'],
            ['Cm', 'Eb'],
            ['Eb', 'Eb'],
            ['Dm', 'F'],
            ['Em', 'G'],
            ['Abm', "B"]
        ]

        for keypair in equal_keypairs:
            self.assertTrue(KeyUtils.are_keys_equal(
                keypair[0], keypair[1]), "{} != {}".format(keypair[0], keypair[1]))


if __name__ == '__main__':
    unittest.main()
