const RecorderController = require ("../Recorder/Recorder.Controller.js");
const SongPickerController = require ("../SongPicker/SongPicker.Controller.js");
const AudioPlayer = require ("../Components/AudioPlayer/AudioPlayer.js");
const S = require ("../Server/Server.js");

class Transposer {
	constructor () {
		var server = new S("127.0.0.1", 5000);
		this.server = server;
		this.spc = new SongPickerController (server, this);
		this.spc.start();
		this.rc = new RecorderController (server, this);
		this.toTranspose;
		this.singalongDOM = document.getElementById("singalong");
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
			this.server.POST("/analyse/" + title + "/" + author, reader.result, false)
			.then(this.handleTransposedSong.bind(this))
			.then(this.finish.bind(this))
			.catch((e) => {
				console.log ("Error: " + e);
			});
		})
	}

	handleTransposedSong (songdata) {
		var target = document.getElementById("transposed");
		var audioEl = AudioPlayer(target, songdata);
		return Promise.resolve();
	}

	finish () {
		this.rc.stop();
		this.singalongDOM.classList.add("current");
		console.log ("End of workflow");
	}
}

module.exports = Transposer;