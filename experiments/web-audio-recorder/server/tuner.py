import transposerutils as utils
def getkey (data):
	tmp = "./tmp/tuner.wav"
	utils.writeWavFile(tmp, data)
	key = utils.findkey(tmp, "midiproperties")
	return key