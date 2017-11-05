import midi
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import argparse
import pprint
pp = pprint.PrettyPrinter(indent=4)


diatonic_scale = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
keys = [np.roll(diatonic_scale, i) for i in range(0, 11)]


# assign more weight to tonal root
tonal_root_weight_addition = 2
seventh_degree_weight_addition = 1.5
root_triad_addition = 1.5

for index, key in enumerate(keys):
  tonal_root = index
  key[tonal_root] += tonal_root_weight_addition

  # 3rd and 5th degree
  key[((index + 1 + 4) % 12) - 1] += root_triad_addition
  key[((index + 1 + 7) % 12) - 1] += root_triad_addition

  # seventh degree
  key[((index + 1 + 11) % 12) - 1] += seventh_degree_weight_addition

pitches = [
            'C',
            'C#',
            'D',
            'D#',
            'E',
            'F',
            'F#',
            'G',
            'G#',
            'A',
            'A#',
            'B'
        ]

class KeyUtils():
    @staticmethod
    def get_all_pitches():
        global pitches
        return pitches

    @staticmethod
    def get_keys():
        global keys
        return keys

    @staticmethod
    def print_keys():
        keys = KeyUtils.get_keys()
        pitches = KeyUtils.get_all_pitches()
        print "key\tnotes"
        for key_index in range(0, len(keys)):
            key_letter = pitches[key_index]
            pitches_numbers = filter(
                lambda scale_degree: keys[key_index][scale_degree] >= 1, range(len(keys[key_index])))
            letters = [pitches[pitch_number]
                       for pitch_number in pitches_numbers]
            print key_letter + "\t" + "\t ".join(letters)
        print "-------------------------------\n"

        print "Weights:\n"
        for key_index in range(0, len(keys)):
            print "Key {},  \t{} notes with weights: \t {}".format(KeyUtils.get_all_pitches()[key_index], len(filter(lambda weight: weight >= 1, keys[key_index])), "\t".join([str(weight) for weight in keys[key_index]]))
        print "-------------------------------\n"

    @staticmethod
    def get_absolute_pitch(pitch_number):
        # https://newt.phys.unsw.edu.au/jw/notes.html
        # C starts on 24
        python_midi_pitch_offset = 26
        return (pitch_number - python_midi_pitch_offset) % 11
    
    @staticmethod
    def pitch_numbers_to_letters(pitch_numbers):
      pitch_letters = KeyUtils.get_all_pitches()
      return [pitch_letters[number] for number in pitch_numbers]

    ##
    #  Converts minor keys to their relative majors,
    #  Converts flats to sharps
    #  Returns lettered key, eg. A#
    ##
    @staticmethod
    def get_standard_key(key):
      #minor to major
      if(key.endswith('m')):
        root_note = key.split('m')[0]
        minor_index = KeyUtils.get_all_pitches().index(root_note)
        major_index = minor_index + 3
        key = KeyUtils.get_all_pitches()[((major_index + 1) % 12) - 1]
      
      #flats to sharps
      if(key.endswith('b')):
        root_note = key.split('b')[0]
        key_index = KeyUtils.get_all_pitches().index(root_note) - 1
        key = KeyUtils.get_all_pitches()[key_index]
           
      return key

    # keys are reduced to standard key and compared
    @staticmethod
    def are_keys_equal(key1, key2):
      return KeyUtils.get_standard_key(key1) == KeyUtils.get_standard_key(key2)



class MidiProperties():
    def __init__(self, filename):
        self.pattern = midi.read_midifile(filename)
        self.filename = filename
        self.pitch_counts = None
        self.notes = None
        self.sanitized_pitch_counts = None

    def get_notes(self):
        if self.notes is None:
            self.notes = []

            for track in self.pattern:
                for event in track:
                    # check that the current event is a NoteEvent, otherwise it won't have the method get_pitch() and we'll get an error
                    if isinstance(event, midi.NoteEvent):
                        pitch_number = event.get_pitch()
                        reduced_pitch_number = KeyUtils.get_absolute_pitch(
                            pitch_number)
                        # print pitch_number, reduced_pitch_number, KeyUtils.get_all_pitches()[reduced_pitch_number]
                        self.notes.append(reduced_pitch_number)
        return self.notes

    def get_pitch_counts(self):
        # count frequencies
        if self.pitch_counts is None:
            self.pitch_counts = np.zeros([len(KeyUtils.get_all_pitches())])

            for reduced_pitch_number in self.get_notes():
                self.pitch_counts[reduced_pitch_number] += 1

        return self.pitch_counts

    def get_notes_count(self):
        return len(self.get_notes())

    def get_sanitized_pitch_counts(self):
        if self.sanitized_pitch_counts is None:

            count_threshold_percentage = 0.05
            count_threshold = max(count_threshold_percentage * self.get_notes_count(), 2)

            self.sanitized_pitch_counts = [
                0 if song_pitch_count <= count_threshold else song_pitch_count for song_pitch, song_pitch_count in enumerate(self.get_pitch_counts())]

        return self.sanitized_pitch_counts

    def get_similar_keys(self, normalize=False):
        key_similarities = cosine_similarity([self.get_pitch_counts()], KeyUtils.get_keys())[0]
        keys_sorted_indexes = np.argsort(key_similarities)
        keys_sorted_indexes = np.flip(keys_sorted_indexes, 0)
        return (keys_sorted_indexes , [key_similarities[i] for i in keys_sorted_indexes])
          


if __name__ == "__main__":
    KeyUtils.print_keys()
    exit()
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="Path to input midi file.")
    args = parser.parse_args()

    KeyUtils.print_keys()

    midi_properties = MidiProperties(args.infile)

    print "{}\t: {}".format("Pitches\t\t", "\t".join(KeyUtils.get_all_pitches()))
    print "{}\t: {}".format("Pitch Counts\t", "\t".join([str(p) for p in midi_properties.get_pitch_counts()]))
    print "{}\t: {}".format("Sanitized Counts", "\t".join([str(p) for p in midi_properties.get_sanitized_pitch_counts()]))
    print "{}\t: {}".format("Sanitized pitches", "\t".join([KeyUtils.get_all_pitches()[pitch_number] if pitch_count > 0 else '-' for pitch_number, pitch_count in enumerate(midi_properties.get_sanitized_pitch_counts())]))

    # find similarities

    print "\nResults"
    keys_sorted_indexes, key_similarities = midi_properties.get_similar_keys()
    for sort_index, key_similarity in enumerate(key_similarities):
        print "{}\t: {}".format(pitches[keys_sorted_indexes[sort_index]], key_similarity)
    