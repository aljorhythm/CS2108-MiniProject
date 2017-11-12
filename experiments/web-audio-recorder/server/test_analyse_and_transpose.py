from transposerutils import *

song = {
  "voice" : 'src/songs/B-ThinkingOutLoud_vocals_original_melodia.mid',
  "original" : 'src/songs/D-ThinkingOutLoud_original.mp3',
  'output_dir' : 'src/transposed'
}

print findkey(song["voice"])

print analyseandtranspose(song["voice"], song["original"], song["output_dir"])