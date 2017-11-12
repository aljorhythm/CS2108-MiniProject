import transposerutils as utils

import os
import librosa
from audio_to_midi_melodia import audio_to_midi_melodia
from subprocess import call

def songlist():
	return utils.songlist()

def convert_to_midi(filepath):
	midi_dir = "./src/songs"
	filepath = os.path.abspath(filepath)
	filepath_wo_ext = filepath.replace('.wav', '')
	filename_wo_ext = os.path.basename(filepath_wo_ext)
	options = {'suffix': '', 'args': []}
	args = options["args"]
	suffix = options['suffix']
	output_filepath = "{}{}{}.{}".format(midi_dir, filename_wo_ext, "_melodia" + ("_" + suffix if suffix != "" else ""), "mid")
	if not os.path.isfile(output_filepath):
		print "converting {} to {} with args {}".format(filepath, output_filepath, args)
		bpm = utils.audio_to_bpm(filepath)
		audio_to_midi_melodia(filepath, output_filepath, bpm)
	return output_filepath
	
def process_recording (title, author, data):
	output_dir = "./src/transposed"
	recording_path = "./tmp/file.wav"
	songs_path = "./src/songs"
	original_path = utils.findsongpath(songs_path, title, author);
	utils.writeWavFile(recording_path, data)

	recording_midi = convert_to_midi(original_path)
	info = utils.analyseandtranspose(recording_midi, original_path, output_dir)

	return recording_path, info['output_path'], info['key']

def fullsong (title, author):
	path = "./src/songs"
	url = utils.findsongpath(path, title, author)
	key, _title, _author = utils.infofromurl(url)
	return url, key

def shortsong (title, author):
	path = "./src/songs"
	url = utils.findsongpath(path, title, author)
	key, _title, _author = utils.infofromurl(url)
	return url, key


