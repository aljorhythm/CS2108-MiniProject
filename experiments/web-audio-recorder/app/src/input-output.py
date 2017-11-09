import argparse

def main (names):
	print (names)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument ("names", nargs="+", help="List of names")
	args = parser.parse_args()
	main(args.names)