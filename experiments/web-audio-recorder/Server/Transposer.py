import transposerutils as utils

def songlist ():
	return utils.songlist()

def process_recording (title, author, data):
	recording_path = "./tmp/file.wav"
	songs_path = "./src/songs"
	original_path = utils.findsongpath(songs_path, title, author);
	utils.writeWavFile(recording_path, data)
	output_path = utils.analyseandtranspose(recording_path, original_path)

	return output_path

def shortsong (title, author):
	path = "./src/songs"
	return utils.findsongdata(path, title, author)


