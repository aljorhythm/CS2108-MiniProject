import transposerutils
import midi_properties
import os
from multiprocessing import Process, Manager, Lock
import time

mutex = Lock()

def task (output_dir, original_path, new_key, original_key):
	output_path, steps = transposer.transpose_to_key (output_dir, original_path, new_key, original_key)
	expected_key = new_key
	actual_key = transposerutils.findkey(output_path)

	print "Expected: {}\tActual: {}".format(expected_key, actual_key)

def runtest ():
	songs_dir = "./src/songs"
	transposed_dir = "./src/transposed"
	result = {"correct": 0, "wrong": 0}
	for filename in os.listdir(songs_dir):
		if filename.endswith(".wav") or filename.endswith("mp3"):
			original_key = transposerutils.findkey("/".join([songs_dir, filename]))
			for key in midi_properties.pitches
			task (transposed_dir, filename, key, original_key)


if __name__ == '__main__':
	runtest()