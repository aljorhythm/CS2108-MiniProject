import subprocess
import numpy as np
import urllib
import base64
import os
import librosa
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

def readsong (src):
	return wavfile.read(src)

def keyfindercli (src):
	return subprocess.check_output(["keyfinder-cli", src]).strip()

def parseBase64Audio (data):
	return data[data.find(",")+1:].decode("base64")

def songlist ():
	path = "./src/songs"
	filenames = []
	for filename in os.listdir(path):
		if filename.endswith(".wav") or filename.endswith("mp3"):
			sep = filename.find("-") #seperator
			author = filename[:sep].strip()
			title = filename[sep + 1:].strip()
			filenames.append({
					"author": author,
					"title": title
				})
	return filenames

def findsongpath (path, title, author):
	for filename in os.listdir(path):
		if filename.endswith(".wav") or filename.endswith("mp3"):
			sep = filename.find("-") #seperator
			if author == filename[:sep].strip() and title == filename[sep + 1:].strip():
				return "%s/%s" % (path, filename)

def findsongdata (path, title, author):
	songpath = findsongpath(path, title, author)
	data = open(songpath, "rb").read()
	return data

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
