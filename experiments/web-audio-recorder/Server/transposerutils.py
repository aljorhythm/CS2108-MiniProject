import subprocess
import numpy as np
import urllib
import base64
import os
import librosa

from wavmidi import convert_to_midi
from midi_properties import MidiProperties, KeyUtils

# Key Extraction
key_detection_tools = {
	".mid" : "midiproperties",
	".mp3" : "filename", #"keyfindercli",
	".wav" : "filename"
}

def findkey(src, method=None):
	ext = os.path.splitext(src)[1]
	if method is None:
		method = key_detection_tools[ext]

	if method == "keyfindercli":
		key = keyfindercli(src)
	elif method == "filename":
		key = filenamekey(src)
	elif method == "midiproperties":
		key = midikeyfinder(src)

	return key

def filenamekey (src):
	src = os.path.basename(src)
	key = src.split("-")[0]
	return key

def midikeyfinder (src):
	midi_properties = MidiProperties(src)
	key_numbers, similarities = midi_properties.get_similar_keys()
	key = key_numbers[0]
	key = KeyUtils.get_all_pitches()[key]
	return key

def keyfindercli (src):
	return subprocess.check_output(["keyfinder-cli", src]).strip()

# Base64 File Handling
def parseBase64Audio (data):
	return data[data.find(",")+1:].decode("base64")

def writeWavFile (path, data):
	f = open(path, "wb+")
	f.write(parseBase64Audio(data))
	f.close();

# Song Path 
def songlist ():
	path = "./src/songs"
	filenames = []
	for filename in sorted(os.listdir(path)):
		if filename.endswith(".wav") or filename.endswith("mp3"):
			key, author, title = infofromurl(filename)
			filenames.append({
				"author": author,
				"title": title,
				"key": key
			})
	return filenames

def findsongpath (path, title, author):
	# Return the path of the song given the title and author from given directory `path`
		for filename in os.listdir(path):
			if filename.endswith(".wav") or filename.endswith("mp3"):
				src_key, src_author, src_title = infofromurl(filename)
				if author == src_author and title == src_title:
					return "%s/%s" % (path, filename)

def infofromurl (url):
	return infofromfilename(os.path.basename(url))

def infofromfilename (filename):
	info = filename.split("-")

	key = info[0].strip().upper()
	if len(info) >= 3:
		author = info[1].strip()
		title = info[2].strip()
	else:
		author = ""
		title = info[1].strip()
	return key, author, title


# Analysing and Transposing 

def analyseandtranspose (recording_path, original_path, output_dir):

	original_key = findkey(original_path) #"keyfindercli")
	recording_key = findkey(recording_path) #, "keyfindercli")

	output_path, steps = transpose_to_key (output_dir, original_path, recording_key, original_key)

	return {
		"original_path" : original_path,
		"output_path" : output_path,
		"steps" : steps,
		"key" : recording_key
	}

def transpose_to_key (output_dir, original_path, new_key, original_key):
	output_path = transposed_output_path (output_dir, new_key, original_path)
	steps = calculate_transpose_steps (original_key, new_key)
	transpose (original_path, output_path, steps)

	print "\n=================== Analyse and Transpose Log ==================="
	print "Key of Original '{}': {}".format(os.path.basename(original_path), original_key)	
	print "Key of Recording : {}".format(new_key)
	print "Output file:\t {}".format(output_path)
	print "Steps:\t {}".format(steps)
	print "\n"

	return output_path, steps

def calculate_transpose_steps (original_key, recording_key):
	return -1 * KeyUtils.key_difference(original_key, recording_key)

def transposed_output_path (output_dir, new_key, original_path):
	original_filename = os.path.basename(original_path)
	original_filename_without_key = "-".join(original_filename.split("-")[1:])
	original_filename_without_key_without_ext = ext = os.path.splitext(original_filename_without_key)[0]
	output_path = "{}/{}-{}.wav".format(output_dir, new_key, original_filename_without_key_without_ext)
	return output_path

def transpose (src, out, steps):
	if os.path.isfile(out):
		return
	y, sr = librosa.load(src)
	y_third = librosa.effects.pitch_shift(y, sr, steps)
	librosa.output.write_wav(out, y_third, sr)
