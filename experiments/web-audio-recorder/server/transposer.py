import transposerutils as utils

def songlist():
	return utils.songlist()

def process_recording (title, author, data):
	recording_path = "./tmp/file.wav"
	songs_path = "./src/songs"
	original_path = utils.findsongpath(songs_path, title, author);
	utils.writeWavFile(recording_path, data)
	output_path, key = utils.analyseandtranspose(recording_path, original_path)

	return output_path, key

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


