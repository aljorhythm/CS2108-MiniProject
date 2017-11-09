const Recorder = require ("./Recorder.js");
const FD = require ("form-data");
const Controller = require ("../Controller/Controller.js")

class RecorderController extends Controller {
	constructor (server, transposer) {
		super("recorder");

		this.transposer = transposer;
		this.recorder = new Recorder (server);

		this.startBtn;
		this.stopBtn;
		this.downloadBtn;
		this.player;

		this.initControllers ();
	}

	start (player) {
		super.start();
		this.player = player;
		this.recorder.on();
	}


	initControllers () {
		this.startBtn = this.getButton ("start", this.handleStartBtn);
		this.stopBtn = this.getButton ("stop", this.handleStopBtn);
		this.downloadBtn = this.getButton ("download", this.handleDownloadBtn);
	}

	handleStartBtn () {
		console.log ("Controller: Start"); 
		this.player.play();
		this.recorder.start().catch((err) => {
			console.log(err);
		});
	}

	handleStopBtn () { 
		console.log ("Controller: Stop"); 
		this.player.pause();
		
		this.recorder.stop()
		.then((blob) => {
			this.createDownloadLink(blob);
			this.transposer.recordingDone(blob);
		})
		.catch((err) => {
			console.log(err);
		});
	}

	handleDownloadBtn () { console.log ("Download"); }

	createDownloadLink (blob) {
		// var blob = new Blob (mp3Data, {type: 'audio/mp3'});
		var url = window.URL.createObjectURL(blob);

		const downloadEl = document.createElement('a');
	    downloadEl.style = 'display: block';
	    downloadEl.innerHTML = 'download';
	    downloadEl.download = 'audio.wav';
	    downloadEl.href = url;
	    this.downloadBtn.appendChild(downloadEl);
	}

	
}

module.exports = RecorderController;