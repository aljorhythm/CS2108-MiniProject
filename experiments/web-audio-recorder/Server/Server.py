from flask import Flask, jsonify, Response, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import urllib
import base64
from Transposer import analyseandtranspose

import os

app = Flask(__name__)
CORS(app)

def parseBase64Audio (data):
	return data[data.find(",")+1:].decode('base64')

def makeresponse (code, msg):
	return jsonify({
		"status": code,
		"msg": msg
	})

def songlist ():
	path = "./src/songs"
	filenames = []
	for filename in os.listdir(path):
		if filename.endswith(".wav") or filename.endswith("mp3"):
			sep = filename.find("-") #seperator
			author = filename[:sep].strip()
			title = filename[sep + 1:].strip()
			filenames.append({
					"author": author,
					"title": title
				})
	return filenames

def findsongpath (path, title, author):
	for filename in os.listdir(path):
		if filename.endswith(".wav") or filename.endswith("mp3"):
			sep = filename.find("-") #seperator
			if author == filename[:sep].strip() and title == filename[sep + 1:].strip():
				return filename

def findsongdata (path, title, author):
	songpath = "%s/%s" % (path, findsongpath(path, title, author))
	data = open(songpath, "rb").read()
	return data

def writeWavFile (path, data):
	f = open(path, 'wb+')
	f.write(parseBase64Audio(data))
	f.close();

@app.errorhandler(404)
def page_not_found(e):
	return makeresponse(404, "Page Not Found")

@app.route("/songlist", methods=['GET'])
def get_songlist ():
	return makeresponse(200, songlist())

@app.route("/songlist/<title>/<author>", methods=['GET'])
def get_shortsong (title, author):
	path = "./src/songs"
	return findsongdata(path, title, author)

@app.route("/analyse/<title>/<author>", methods=['POST'])
def post_record(title, author):
	path = "./tmp/file.wav"
	writeWavFile(path, request.data)
	songdata = analyseandtranspose(path, title, author)

	return songdata



if __name__ == '__main__':
	app.run(debug=True)