if [ -z $1 ]; then
	echo "Usage: audio_to_midi.sh <FILENAME>"
	exit 1
fi

INDIR="../mp3/"
OUTDIR="../data/"
INFILE="$1"
OUTFILE="$1.mid"

python2 audio_to_midi_melodia.py $INFILE $OUTFILE $(python2 audio_to_bpm.py $INFILE)
python2 midi_properties.py $OUTFILE