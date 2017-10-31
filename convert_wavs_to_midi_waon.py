# use waon to convert wavs to midi
# wav file will not be converted if midi is found

import os
from subprocess import call

wavs_dir = 'data/'
midi_dir = 'data/'

if not os.path.exists(midi_dir):
    os.makedirs(midi_dir)

for dir_name, dir_list, filelist in os.walk(wavs_dir):
    for filename in [filename for filename in filelist if '.wav' in filename]:
        filepath = wavs_dir + filename
        filepath = os.path.abspath(filepath)
        filepath_wo_ext = filepath.replace('.wav', '')
        filename_wo_ext = os.path.basename(filepath_wo_ext)
        options_list = [
            {'suffix': '', 'args': []},
            # {'suffix': '-b70-n8192',
            #     'args': ["--bottom", "70", "-n", "8192"]},
            # {'suffix': '-b70-t90-n8192',
            #     'args': ["--bottom", "70", "--top", "90", "-n", "8192"]},
            # {'suffix': '-b60-t70-8192',
            #     'args': ["--bottom", "60", "--top", "70", "-n", "8192"]},
            # {'suffix': '-b50-t60-8192',
            #     'args': ["--bottom", "50", "--top", "60", "-n", "8192"]}
        ]
        for options in options_list:
            args = options["args"]
            suffix = options['suffix']
            output_filepath = "{}{}{}.{}".format(midi_dir, filename_wo_ext, "_waon" + ("_" + suffix if suffix != "" else ""), "mid")
            if not os.path.isfile(output_filepath):
                print "converting {} to {} with args {}".format(filepath, output_filepath, args)
                call(["waon", "-i", filepath, "-o", output_filepath] + args)
