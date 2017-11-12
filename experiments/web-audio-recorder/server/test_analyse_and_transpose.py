from ... import transposerutils

song = {
  "voice" : 'src/songs/B-ThinkingOutLoud_vocals_original_melodia.mid',
  "original" : 'src/songs/D-ThinkingOutLoud_original.mp3',
  'output_dir' : 'src/transposed'
}

print transposerutils.findkey(song["voice"])

print transposerutils.analyseandtranspose(song["voice"], song["original"], song["output_dir"])