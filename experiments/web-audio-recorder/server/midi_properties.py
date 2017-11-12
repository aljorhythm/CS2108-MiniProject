import midi
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import argparse
import pprint
pp = pprint.PrettyPrinter(indent=4)

# diatonic_scale = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1] # equal weight for every scale degree
diatonic_scale = [10, 0, 2, 0, 10, 4, 0, 2, 0, 2, 0, 6] # this one has weights

keys = [np.roll(diatonic_scale, i) for i in range(0, 12)]

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

hr = "-----------------------------------------------------------------\n"
hr2 = "******************************************************************\n"

def heading(str):
  print str.center(len(hr2))
  print hr2

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

        heading("Keys")
        print "Scale"
        print "{}\t| {}".format("Degree", "\t".join([str(i + 1) for i in range(0, 7)]))        
        print "Key\t| Notes"
        
        print hr
        for key_index in range(0, len(keys)):
            key_letter = pitches[key_index]
            key_vector = keys[key_index]
            letters = [pitches[pitch_number] if pitch_weight > 0 else ""
                       for pitch_number, pitch_weight in enumerate(key_vector)]
            letters = np.roll(letters, -key_index)
            print key_letter + "\t| " + "\t".join(filter(lambda l : l != "", letters))
        print hr

        heading("Vector (weights)")        
        print "{}\t|\t {}".format("Pitch Class", "\t".join(KeyUtils.get_all_pitches()))
        print "Key"
        print hr
        for key_index in range(0, len(keys)):
            # print "Key {},\t{} notes, weights: \t {}".format(KeyUtils.get_all_pitches()[key_index].ljust(2), len(filter(lambda weight: weight >= 1, keys[key_index])), "\t".join([str(weight) for weight in keys[key_index]]))
            print "{}\t\t| \t {}".format(KeyUtils.get_all_pitches()[key_index].ljust(2), "\t".join([str(weight) for weight in keys[key_index]]))
            
        print hr

    @staticmethod
    def key_difference(a, b):
      a_index =  KeyUtils.get_all_pitches().index(KeyUtils.get_standard_key(a))
      b_index = KeyUtils.get_all_pitches().index(KeyUtils.get_standard_key(b))

      # choose shorter route
      movement1 = a_index + 12 - b_index
      movement2 = a_index - b_index

      res = movement1 if abs(movement1) <= abs(movement2) else movement2
      return res

    @staticmethod
    def get_absolute_pitch(pitch_number):
        # https://newt.phys.unsw.edu.au/jw/notes.html
        # C starts on 24
        python_midi_pitch_offset = 24
        return (pitch_number - python_midi_pitch_offset) % 12
    
    @staticmethod
    def pitch_numbers_to_letters(pitch_numbers):
      pitch_letters = KeyUtils.get_all_pitches()
      return [pitch_letters[number] for number in pitch_numbers]

    #flats to sharps
    @staticmethod
    def flat_to_sharp(note):
      if(note.endswith('b')):
        note = note.split('b')[0]
        key_index = KeyUtils.get_all_pitches().index(note) - 1
        note = KeyUtils.get_all_pitches()[key_index]
      
      return note

    ##
    #  Converts minor keys to their relative majors,
    #  Converts flats to sharps
    #  Returns lettered key, eg. A#
    ##
    @staticmethod
    def get_standard_key(key):
      
      #minor to major
      if(key.endswith('m')):
        root_note = KeyUtils.flat_to_sharp(key.split('m')[0])
        minor_index = KeyUtils.get_all_pitches().index(root_note)
        major_index = minor_index + 3
        key = KeyUtils.get_all_pitches()[((major_index + 1) % 12) - 1]
      else:
        key = KeyUtils.flat_to_sharp(key)
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
        key_numbers = np.argsort(key_similarities)
        key_numbers = np.flip(key_numbers, 0)
        return (key_numbers , [key_similarities[i] for i in key_numbers])
          


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="Path to input midi file.")
    args = parser.parse_args()

    KeyUtils.print_keys()

    heading("File {}".format(args.infile))            
    print "{}\t| {}".format("Pitch Class\t", "\t".join(KeyUtils.get_all_pitches()))

    midi_properties = MidiProperties(args.infile)
    # song
    print "{}\t| {}".format("Pitch Counts\t", "\t".join([str(p) for p in midi_properties.get_pitch_counts()]))
    print "{}\t| {}".format("Sanitized Counts", "\t".join([str(p) for p in midi_properties.get_sanitized_pitch_counts()]))
    print "{}\t| {}".format("Sanitized pitches", "\t".join([KeyUtils.get_all_pitches()[pitch_number] if pitch_count > 0 else '-' for pitch_number, pitch_count in enumerate(midi_properties.get_sanitized_pitch_counts())]))

    # find similarities

    # print [KeyUtils.get_all_pitches()[note] for note in midi_properties.get_notes()]
    print "\nResults"
    key_numbers, key_similarities = midi_properties.get_similar_keys()

    # print key_numbers
    # print key_similarities
    for sort_index, key_similarity in enumerate(key_similarities):
        print "{}\t| {}".format(pitches[key_numbers[sort_index]], key_similarity)
    