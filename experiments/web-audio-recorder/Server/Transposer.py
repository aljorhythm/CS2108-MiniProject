import transposerutils
import numpy as np
import wave
import subprocess
import os
import librosa

def analyseandtranspose (recording_path, original_path):
	output = './tmp/transposed.wav'
	transpose (original_path, output)
	print ("Key of Recording: %s" % findkey(recording_path))
	print ("Key of Original: %s" % findkey(original_path))
	print ("Key of Transposed: %s" % findkey(output))
	return open(output, "rb").read();

def findkey (src):
	key = transposerutils.keyfindercli (src)
	return key

def readsong (src):
	return wavfile.read(src)

def transpose (src, out):
	y, sr = librosa.load(src)
	y_third = librosa.effects.pitch_shift(y, sr, n_steps=1)
	librosa.output.write_wav(out, y_third, sr)

