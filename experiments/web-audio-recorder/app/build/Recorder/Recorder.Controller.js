const Recorder = require ("./Recorder.js");
const FD = require ("form-data");
const Controller = require ("../Controller/Controller.js");

class RecorderController extends Controller {
	constructor (server, transposer) {
		super("recorder");

		this.transposer = transposer;
		this.recorder = new Recorder (server);

		this.startBtn;
		this.stopBtn;
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
	}

	handleStartBtn () {
		console.log ("Controller: Start"); 
		this.player.play();
		this.player.addEventListener("ended", () => {
			console.log("Player Ended! Stopping Recording...");
			this.stopBtn.click();
		})
		this.recorder.start().catch((err) => {
			console.log(err);
		});
	}

	handleStopBtn () { 
		console.log ("Controller: Stop"); 
		this.player.pause();
		this.recorder.stop(() => {
			this.transposer.loading("Analysing and Transposing...");
		})
		.then((blob) => {
			this.transposer.recordingDone(blob);
		})
		.catch((err) => {
			console.log(err);
		});
	}

	handleDownloadBtn () { console.log ("Download"); }


	
}

module.exports = RecorderController;