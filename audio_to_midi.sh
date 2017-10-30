if [ -z $1 ]; then
	echo "Usage: audio_to_midi.sh <FILENAME>"
	exit 1
fi

INDIR="../mp3/"
OUTDIR="../midi/"
INFILE="$INDIR$1.mp3"
OUTFILE="$OUTDIR$1.mid"

python audio_to_midi_melodia.py $INFILE $OUTFILE $(python audio_to_bpm.py $INFILE)