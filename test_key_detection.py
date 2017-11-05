import unittest
import os
import subprocess

from midi_properties import MidiProperties
from midi_properties import KeyUtils

class TestKeyDetection(unittest.TestCase):

    def test_libkeyfinder(self):
        print "************************************"      
        
        midi_dir = 'data/'

        if not os.path.exists(midi_dir):
            os.makedirs(midi_dir)
        errors = []
        success = []
        for dir_name, dir_list, filelist in os.walk(midi_dir):
            for filename in [filename for filename in filelist if filename.endswith('.mp3')]:
                filepath = midi_dir + filename
                expected_key = filename.split("-")[0]
                most_similar_key = subprocess.check_output(['keyfinder-cli', filepath]).strip()
                if not KeyUtils.are_keys_equal(most_similar_key, expected_key):
                    errors.append({
                        "filepath": filepath,
                        "expected": expected_key,
                        "results": KeyUtils.get_standard_key(most_similar_key)
                    })
                else:
                    success.append(filepath)

        total = len(success) + len(errors)
        success_count = len(success)
        percentage = success_count * 100.0 / total
        print "LibKeyFinder: \t{} correct out of {}, {}%".format(len(success), total, percentage)
        print "Correct Results:\n" + "\n".join(success)

        msg = "\nWrong Results:\n{}" .format("\n".join(["{} :\t expected {},  \tactual {}".format(err["filepath"].ljust(40, ' '), err["expected"], err["results"]) for err in sorted(errors, key = lambda err: err["filepath"])]))
        self.assertEqual(errors, [], msg = msg)

        print "************************************\n\n"


    def test_midi_properties(self):
        print "************************************"    
      
        midi_dir = 'data/'

        if not os.path.exists(midi_dir):
            os.makedirs(midi_dir)
        errors = []
        success = []
        for dir_name, dir_list, filelist in os.walk(midi_dir):
            for filename in [filename for filename in filelist if filename.endswith('.mid')]:
                filepath = midi_dir + filename
                expected_key = filename.split("-")[0]
                midi_properties = MidiProperties(filepath)
                key_sorted_indexes, key_similarities = midi_properties.get_similar_keys()
                most_similar_key = KeyUtils.get_all_pitches()[
                    key_sorted_indexes[0]]
                if not KeyUtils.are_keys_equal(most_similar_key, expected_key):
                    results = KeyUtils.pitch_numbers_to_letters(key_sorted_indexes)
                    errors.append({
                        "filepath": filepath,
                        "results": results,
                        "incorrect_rank" : results.index(KeyUtils.get_standard_key(expected_key)) + 1,
                        "expected_key": expected_key
                    })
                else:
                    success.append(filepath)

        total = len(success) + len(errors)
        success_count = len(success)
        percentage = success_count * 100.0 / total
        print "MidiProperties:\t{} correct out of {}, {}%".format(success_count, total, percentage)

        print "Correct Results:\n" + "\n".join(success)
        msg = "\nWrong Results:\n" + "\n".join(["{} Incorrect rank of {}\t: {},\t{}".format(err["filepath"].ljust(90), err["expected_key"], err["incorrect_rank"], "\t".join(err["results"])) for err in sorted(errors, key = lambda err: err["filepath"])])
        
        self.assertEqual(errors, [], msg = msg)

        print "************************************\n\n"

if __name__ == '__main__':
    unittest.main()
