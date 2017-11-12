import subprocess
import numpy as np
import urllib
import base64
import os
import librosa

def findkey (src):
	key = keyfindercli (src)
	return key

def keyfindercli (src):
	return subprocess.check_output(['keyfinder-cli', src]).strip()

def parseBase64Audio (data):
	return data[data.find(",")+1:].decode('base64')

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
	f = open(path, 'wb+')
	f.write(parseBase64Audio(data))
	f.close();

def analyseandtranspose (recording_path, original_path):
	output = './tmp/transposed.wav'
	transpose (original_path, output)
	key = findkey(output)
	print ("Key of Recording: %s" % findkey(recording_path))
	print ("Key of Original: %s" % findkey(original_path))
	print ("Key of Transposed: %s" % key)
	return output, key


def transpose (src, out):
	y, sr = librosa.load(src)
	y_third = librosa.effects.pitch_shift(y, sr, n_steps=1)
	librosa.output.write_wav(out, y_third, sr)