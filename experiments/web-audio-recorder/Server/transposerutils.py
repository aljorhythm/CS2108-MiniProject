import subprocess
import numpy as np
import urllib
import base64
import os
import librosa

def findkey (src):
	key = keyfindercli (src)
	return key

def readsong (src):
	return wavfile.read(src)

def keyfindercli (src):
	return subprocess.check_output(['keyfinder-cli', src]).strip()

def parseBase64Audio (data):
	return data[data.find(",")+1:].decode('base64')

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
	f = open(path, 'wb+')
	f.write(parseBase64Audio(data))
	f.close();

def analyseandtranspose (recording_path, original_path):
	output = './tmp/transposed.wav'
	transpose (original_path, output)
	print ("Key of Recording: %s" % findkey(recording_path))
	print ("Key of Original: %s" % findkey(original_path))
	print ("Key of Transposed: %s" % findkey(output))
	return open(output, "rb").read();


def transpose (src, out):
	y, sr = librosa.load(src)
	y_third = librosa.effects.pitch_shift(y, sr, n_steps=1)
	librosa.output.write_wav(out, y_third, sr)