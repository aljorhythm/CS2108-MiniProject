# use waon to convert wavs to midi

import os
from subprocess import call

wavs_dir = '../wav-files/'

for dir_name, dir_list, filelist in os.walk(wavs_dir):
  for filename in filelist:
    filepath = wavs_dir + filename
    filepath = os.path.abspath(filepath)
    filepath_wo_ext = filepath.replace('.wav', '')
    filename_wo_ext = os.path.basename(filepath_wo_ext)
    output_filepath = 'midis/' + filename_wo_ext + ".mid"
    print "converting {} to {}".format(filepath, output_filepath)
    print " ".join(["waon", "-i", filepath, "-o", output_filepath])
    call(["waon", "-i", filepath, "-o", output_filepath])

    