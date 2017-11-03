const Recorder = require ("./Recorder.js");
class RecorderController {
	constructor () {

		this.startBtn;
		this.stopBtn;
		this.downloadBtn;

		this.initControllers ();

		this.recorder = new Recorder ();
		this.recorder.on();
	}


	initControllers () {
		var getButton =  (id, onClick) => {
			var btn = document.getElementById(id);
			btn.addEventListener ("click", onClick.bind(this));
			return btn;
		}
		this.startBtn = getButton ("start", this.handleStartBtn);
		this.stopBtn = getButton ("stop", this.handleStopBtn);
		this.downloadBtn = getButton ("download", this.handleDownloadBtn);
	}

	handleStartBtn () {
		console.log ("Controller: Start"); 
		this.recorder.start();
	}

	handleStopBtn () { 
		console.log ("Controller: Stop"); 
		
		this.recorder.stop().then(this.createDownloadLink.bind(this));
	}

	handleDownloadBtn () { console.log ("Download"); }

	createDownloadLink (mp3Data) {
		var blob = new Blob (mp3Data, {type: 'audio/mp3'});
		var url = window.URL.createObjectURL(blob);

		const downloadEl = document.createElement('a');
	    downloadEl.style = 'display: block';
	    downloadEl.innerHTML = 'download';
	    downloadEl.download = 'audio.mp3';
	    downloadEl.href = url;
	    this.downloadBtn.appendChild(downloadEl);
	}
}

module.exports = RecorderController;