from flask import Flask, jsonify, Response, request, jsonify, send_from_directory
from flask_cors import CORS

import transposer
import tuner

app = Flask(__name__)
CORS(app)

def makeresponse (code, msg):
	return jsonify({
		"status": code,
		"msg": msg
	})

@app.errorhandler(404)
def page_not_found(e):
	return makeresponse(404, "Page Not Found")

@app.route("/songlist", methods=['GET'])
def get_songlist ():
	return makeresponse(200, transposer.songlist())

@app.route("/songlist/<title>/<author>", methods=['GET'])
def get_shortsong (title, author):
	url, key = transposer.shortsong(title, author)
	return makeresponse(200, url)

@app.route("/analyse/<title>/<author>", methods=['POST'])
def post_record(title, author):
	original_url, original_key = transposer.fullsong(title, author)
	transposed_url, transposed_key = transposer.process_recording(title, author, request.data)
	return makeresponse(200, {
		"original": {
			"url" : original_url, 
			"key" : original_key
		}, 
		"transposed": {
			"url": transposed_url, 
			"key": transposed_key
		}
	})

@app.route("/tmp/<file>", methods=['GET'])
def send_tmpfile (file):
	return send_from_directory(directory="tmp", filename=file)

@app.route("/src/songs/<file>", methods=['GET'])
def send_shortsong (file):
	return send_from_directory(directory="src/songs", filename=file)

@app.route("/tuner", methods=['POST'])
def post_tuner ():
	return makeresponse(200, tuner.getkey(request.data))

if __name__ == '__main__':
	app.run(debug=True)