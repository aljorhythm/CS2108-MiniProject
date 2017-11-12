import os
import librosa
from audio_to_midi_melodia import audio_to_midi_melodia
from subprocess import call

def audio_to_bpm(infile):
	y, sr = librosa.load(infile)
	tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
	return int(tempo)

def convert_to_midi(filepath, replace=True):
	midi_dir = "./src/songs/"
	filepath = os.path.abspath(filepath)
	filepath_wo_ext = filepath.replace('.wav', '')
	filename_wo_ext = os.path.basename(filepath_wo_ext)
	options = {'suffix': '', 'args': []}
	args = options["args"]
	suffix = options['suffix']
	output_filepath = "{}{}{}.{}".format(midi_dir, filename_wo_ext, "_melodia" + ("_" + suffix if suffix != "" else ""), "mid")
	if replace or not os.path.isfile(output_filepath):
		print "converting {} to {} with args {}".format(filepath, output_filepath, args)
		bpm = audio_to_bpm(filepath)
		audio_to_midi_melodia(filepath, output_filepath, bpm)
	return output_filepath