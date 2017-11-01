import unittest
import os
import subprocess


class TestLibKeyFinder(unittest.TestCase):

    def test(self):
        midi_dir = 'data/'

        if not os.path.exists(midi_dir):
            os.makedirs(midi_dir)
        errors = []
        success = []
        for dir_name, dir_list, filelist in os.walk(midi_dir):
            for filename in [filename for filename in filelist if filename.endswith('.mp3')]:
                filepath = midi_dir + filename
                print "Checking {}".format(filepath)
                expected_key = filename.split("-")[0]
                most_similar_key = subprocess.check_output(['keyfinder-cli', filepath]).strip()
                if most_similar_key != expected_key:
                    errors.append({
                        "filepath": filepath,
                        "expected": expected_key,
                        "results": most_similar_key
                    })
                else:
                    success.append(filepath)
        print "Correct Results:\n" + "\n".join(success)
        msg = "\nWrong Results:\n" + "\n".join([err["filepath"] + ", expected " + err["expected"] + "\n" + err["results"] for err in errors])
        self.assertEqual(errors, [], msg = msg)

if __name__ == '__main__':
    unittest.main()
