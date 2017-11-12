const Controller = require("../Controller/Controller.js");
const RecorderController = require ("../Recorder/Recorder.Controller.js");
const SongPickerController = require ("../SongPicker/SongPicker.Controller.js");
const AudioPlayer = require ("../Components/AudioPlayer/AudioPlayer.js");
const Loading = require ("../Components/Loading/Loading.js");
const S = require ("../Server/Server.js");
const path = require ("path");

class Transposer extends Controller{
	constructor () {
		super ();

		var server = new S("127.0.0.1", 5000);
		this.server = server;
		this.loadingAnimation = new Loading("loading");
		this.toTranspose;
		this.singalongDOM = document.getElementById("singalong");
		
		this.spc = new SongPickerController (server, this);
		this.spc.start();
		this.rc = new RecorderController (server, this);
	}

	songpickerDone (song, player) {
		this.toTranspose = song;
		this.spc.stop();
		this.rc.start(player);
	}

	recordingDone (blob) {
		this.sendAudioBlobToServer(blob);
	}

	sendAudioBlobToServer (blob) {
		var author = this.toTranspose.author;
		var title = this.toTranspose.title;

		var reader = new FileReader();
		reader.readAsDataURL(blob);
		reader.addEventListener("load", () => {
			var url = "/analyse/" + title + "/" + author;
			if (author.length < 1)
				url = "/analyse/" + title;
			
			this.server.POST(url, reader.result)
			.then(this.handleTransposedSong.bind(this))
			.then(this.finish.bind(this))
			.catch((e) => {
				console.log ("Error: " + e);
			});
		})
	}

	handleTransposedSong (songdata) {

		var data = songdata.msg,

		original_url = this.server.filepath(data.original.url),
		original_key = data.original.key,

		transposed_url = this.server.filepath(data.transposed.url),
		transposed_key = data.transposed.key,

		recorded_url = this.server.filepath(data.recording.url)

		this.setInnerHTML("original-key", original_key);
		this.setInnerHTML("transposed-key", transposed_key);
			
		var originalDOM = document.getElementById("original");
		var transposedDOM = document.getElementById("transposed");
		var recordedDOM = document.getElementById("recorded");

		this.loading("Loading audio player");
		var audioplayerpromise = [];
		audioplayerpromise.push();

		AudioPlayer(originalDOM, original_url)
		.then (() => {
			return AudioPlayer(transposedDOM, transposed_url);
		})
		.then (() => {
			return AudioPlayer(recordedDOM, recorded_url);
		})
		.then(() => {
			this.loadend();
		})



		

		return Promise.resolve();
	}

	finish () {
		this.rc.stop();
		this.singalongDOM.classList.add("current");
		console.log ("End of workflow");
	}

	loading (msg) {
		this.loadingAnimation.show(msg);
	}

	loadend () {
		this.loadingAnimation.hide();
	}
}

module.exports = Transposer;