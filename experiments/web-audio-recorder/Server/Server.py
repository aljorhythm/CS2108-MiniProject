from flask import Flask, jsonify, Response, request, jsonify, send_from_directory
from flask_cors import CORS

import transposer

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
	return makeresponse(200, transposer.shortsong(title, author))

@app.route("/analyse/<title>/<author>", methods=['POST'])
def post_record(title, author):
	transposed_url = transposer.process_recording(title, author, request.data)
	return makeresponse(200, transposed_url)

@app.route("/tmp/<file>", methods=['GET'])
def send_tmpfile (file):
	return send_from_directory(directory="tmp", filename=file)

@app.route("/src/songs/<file>", methods=['GET'])
def send_shortsong (file):
	return send_from_directory(directory="src/songs", filename=file)



if __name__ == '__main__':
	app.run(debug=True)