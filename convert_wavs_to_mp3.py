# requires ffmpeg

import os
import librosa
from subprocess import call

wavs_dir = 'data/'
midi_dir = 'data/'

# use melodia

if not os.path.exists(midi_dir):
    os.makedirs(midi_dir)

for dir_name, dir_list, filelist in os.walk(wavs_dir):
    for filename in [filename for filename in filelist if '.wav' in filename]:
        filepath = wavs_dir + filename
        filepath = os.path.abspath(filepath)
        filepath_wo_ext = filepath.replace('.wav', '')
        filename_wo_ext = os.path.basename(filepath_wo_ext)
        output_filepath = "{}{}.{}".format(midi_dir, filename_wo_ext, "mp3")
        if not os.path.isfile(output_filepath):
            print "converting {} to {}".format(filepath, output_filepath)
            call(["ffmpeg", "-i", filepath, "-codec:a", "libmp3lame", "-qscale:a", "2", output_filepath])