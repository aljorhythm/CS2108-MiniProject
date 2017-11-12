import subprocess
import numpy as np
import urllib
import base64
import os
import librosa
<<<<<<< HEAD
from midi_properties import MidiProperties, KeyUtils

key_detection_tools = {
	".mid" : "midiproperties",
	".mp3" : "keyfindercli",
	".wav" : "filename"
}

def findkey(src):
	ext = os.path.splitext(src)[1]
	method = key_detection_tools[ext]
	if method == "keyfindercli":
		key = keyfindercli(src)
	if method == "filename":
		key = src.split("-")[0]
	if method == "midiproperties":
		midi_properties = MidiProperties(src)
		key_numbers, similarities = midi_properties.get_similar_keys()
		key = key_numbers[0]
		key = KeyUtils.get_all_pitches()[key]
	return key

def keyfindercli (src):
	return subprocess.check_output(["keyfinder-cli", src]).strip()

def parseBase64Audio (data):
	return data[data.find(",")+1:].decode("base64")
=======

def findkey (src):
	key = keyfindercli (src)
	return key

def keyfindercli (src):
	return subprocess.check_output(['keyfinder-cli', src]).strip()

def parseBase64Audio (data):
	return data[data.find(",")+1:].decode('base64')
>>>>>>> 2be2296e8e2223512f68c727fa35109c01ecc323

def songlist ():
	path = "./src/songs"
	filenames = []
	for filename in os.listdir(path):
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
	author = info[1].strip()
	title = info[2].strip()
	return key, author, title

def writeWavFile (path, data):
	f = open(path, "wb+")
	f.write(parseBase64Audio(data))
	f.close();

def analyseandtranspose (recording_path, original_path, output_dir):
  	original_key = findkey(original_path)
	original_filename = os.path.basename(original_path)
	original_filename_without_key = "".join(original_filename.split("-")[1:])
	recording_key = findkey(recording_path)
	new_key = recording_key
	original_filename_without_key_without_ext = ext = os.path.splitext(original_filename_without_key)[0]
	output_path = "{}/{}-{}.wav".format(output_dir, new_key, original_filename_without_key_without_ext)

	steps = -1 * KeyUtils.key_difference(original_key, recording_key)
	
	print "Key of Original: {}".format(original_key)	
	print "Key of Recording: {}".format(recording_key)
	print "Output file:\t {}".format(output_path)
	print "Steps:\t {}".format(steps)
	if not os.path.isfile(output_path):
		transpose (original_path, output_path, steps)
		
	return {
		"original_path" : original_path,
		"output_path" : output_path,
		"steps" : steps
	}
	# return open(output, "rb").read();

def transpose (src, out, steps):
	y, sr = librosa.load(src)
	y_third = librosa.effects.pitch_shift(y, sr, steps)
	librosa.output.write_wav(out, y_third, sr)
