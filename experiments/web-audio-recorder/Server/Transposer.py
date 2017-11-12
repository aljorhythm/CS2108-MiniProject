import transposerutils as utils

def songlist ():
	return utils.songlist()

def process_recording (title, author, data):
	recording_path = "./tmp/file.wav"
	songs_path = "./src/songs"
	output_dir = './src/transposed'
	original_path = utils.findsongpath(songs_path, title, author)
	utils.writeWavFile(recording_path, data)
	info = utils.analyseandtranspose(recording_path, original_path, output_dir)

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


