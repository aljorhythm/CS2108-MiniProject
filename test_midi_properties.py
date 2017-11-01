import unittest
from midi_properties import MidiProperties
from midi_properties import KeyUtils

import os


class TestMidiProperties(unittest.TestCase):

    def test_midi_properties(self):
        midi_dir = 'data/'

        if not os.path.exists(midi_dir):
            os.makedirs(midi_dir)
        errors = []
        success = []
        for dir_name, dir_list, filelist in os.walk(midi_dir):
            for filename in [filename for filename in filelist if '.mid' in filename]:
                filepath = midi_dir + filename
                print "Checking {}".format(filepath)
                expected_key = filename.split("-")[0]
                midi_properties = MidiProperties(filepath)
                key_sorted_indexes, key_similarities = midi_properties.get_similar_keys()
                most_similar_key = KeyUtils.get_all_pitches()[
                    key_sorted_indexes[0]]
                if most_similar_key != expected_key:
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
