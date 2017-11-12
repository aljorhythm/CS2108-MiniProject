import transposerutils
import os
from midi_properties import MidiProperties, KeyUtils
from threading import Thread
import time

def transpose (transposed_dir, filename, new_key, original_key):
	output_path, steps = transposerutils.transpose_to_key (transposed_dir, filename, new_key, original_key)
	print "Transposed: \t{}".format(output_path)

def find_original_key (songs_dir, filename, transposed_dir):
	filename = "/".join([songs_dir, filename])
	original_key = transposerutils.findkey(filename)
	tids = []
	for key in KeyUtils.get_all_pitches():
		tid = Thread(target=transpose, args=(transposed_dir, filename, key, original_key))
		tids.append(tid)
		tid.start()

	for tid in tids:
		tid.join()

def transpose_all ():
	songs_dir = "./src/songs"
	transposed_dir = "./src/transposed"
	tids = []

	for filename in os.listdir(songs_dir):
		if filename.endswith(".wav") or filename.endswith("mp3"):
			tid = Thread(target=find_original_key, args=(songs_dir, filename, transposed_dir))
			tids.append(tid);
			tid.start()

	for tid in tids:
		tid.join()



if __name__ == '__main__':
	start_time = time.time()
	transpose_all()
	print("--- %s seconds ---" % (time.time() - start_time))