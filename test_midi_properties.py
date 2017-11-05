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

    def test_midi_properties(self):
        midi_dir = 'data/'

        if not os.path.exists(midi_dir):
            os.makedirs(midi_dir)
        errors = []
        success = []
        for dir_name, dir_list, filelist in os.walk(midi_dir):
            for filename in [filename for filename in filelist if filename.endswith('.mid')]:
                filepath = midi_dir + filename
                print "Checking {}".format(filepath)
                expected_key = filename.split("-")[0]
                midi_properties = MidiProperties(filepath)
                key_sorted_indexes, key_similarities = midi_properties.get_similar_keys()
                most_similar_key = KeyUtils.get_all_pitches()[
                    key_sorted_indexes[0]]
                if not KeyUtils.are_keys_equal(most_similar_key, expected_key):
                    errors.append({
                        "filepath": filepath,
                        "results": KeyUtils.pitch_numbers_to_letters(key_sorted_indexes)
                    })
                else:
                    success.append(filepath)
        print "Correct Results:\n" + "\n".join(success)
        msg = "\nWrong Results:\n" + "\n".join([err["filepath"] + "\n" + "\t".join(err["results"]) for err in errors])
        self.assertEqual(errors, [], msg = msg)

if __name__ == '__main__':
    unittest.main()
