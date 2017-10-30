import librosa
import argparse

def audio_to_bpm(infile):
	y, sr = librosa.load(infile)
	tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
	return int(tempo)

def main(infile):
	return audio_to_bpm(infile)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("infile", help="Path to input audio file.")
	args = parser.parse_args()
	print(main(args.infile))