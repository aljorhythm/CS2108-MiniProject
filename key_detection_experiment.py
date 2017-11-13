import os
import subprocess

from midi_properties import MidiProperties
from midi_properties import KeyUtils

import json

def keylibfinder(filepath):
    return subprocess.check_output(['keyfinder-cli', filepath]).strip()


def format_results(results):
    libkeyfinder_results = filter(lambda r : r["library"] == 'libkeyfinder', results)
    libkeyfinder_success = filter(lambda r: r["expected"] == r["actual"], libkeyfinder_results)
    libkeyfinder_failures = filter(lambda r: r["expected"] != r["actual"], libkeyfinder_results)

    print len(libkeyfinder_success), len(libkeyfinder_failures), len(libkeyfinder_results), len(libkeyfinder_success)  * 100.0 / len(libkeyfinder_results)

    waon_results = filter(lambda r: 'waon' in r["filepath"], results)
    midi_properties_results = filter(lambda r : r["library"] == 'midi_properties', waon_results)
    midi_properties_success = filter(lambda r: r["expected"] == r["actual"], midi_properties_results)
    midi_properties_failures = filter(lambda r: r["expected"] != r["actual"], midi_properties_results)

    print len(midi_properties_success), len(midi_properties_failures), len(midi_properties_results), len(midi_properties_success)  * 100.0 / len(midi_properties_results)

    melodia_results = filter(lambda r: 'melodia' in r["filepath"], results)
    midi_properties_results = filter(lambda r : r["library"] == 'midi_properties', melodia_results)
    midi_properties_success = filter(lambda r: r["expected"] == r["actual"], midi_properties_results)
    midi_properties_failures = filter(lambda r: r["expected"] != r["actual"], midi_properties_results)

    print len(midi_properties_success), len(midi_properties_failures), len(midi_properties_results), len(midi_properties_success)  * 100.0 / len(midi_properties_results)

results_filename = 'results.txt'
if os.path.isfile(results_filename):
    results = open(results_filename, "r").read()
    results = json.loads(results)
    format_results(results)
else:
    data_dir = 'data/'
    results = []
    for dir_name, dir_list, filelist in os.walk(data_dir):
        for filename in filelist:
            filepath = data_dir + filename
            expected_key = filename.split("-")[0]
            ext = os.path.splitext(os.path.basename(filename))[1]

            if(ext == '.mp3'):
                most_similar_key = keylibfinder(filepath)
                results.append({
                    "filepath": filepath,
                    "expected": KeyUtils.get_standard_key(expected_key),
                    "actual": KeyUtils.get_standard_key(most_similar_key),
                    "library": 'libkeyfinder'
                })

            if(ext == '.mid'):
                midi_properties = MidiProperties(filepath)
                key_sorted_indexes, key_similarities = midi_properties.get_similar_keys()
                most_similar_key = KeyUtils.get_all_pitches()[
                    key_sorted_indexes[0]]
                results.append({
                    "filepath": filepath,
                    "actual": KeyUtils.get_standard_key(KeyUtils.pitch_numbers_to_letters(
                        key_sorted_indexes)[0]),
                    "expected": KeyUtils.get_standard_key(expected_key),
                    'library': 'midi_properties'
                })

    print json.dumps(results)
