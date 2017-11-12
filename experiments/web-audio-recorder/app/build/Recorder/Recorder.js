const LameJs = require ("lameJs");
const RecorderWorker = require ("./Recorder.Worker.js");

const OFF = -1;
const RECORDING = 1;
const IDLE = 0;

class Recorder {
	constructor () {

		this.state;
		this.stream;
		this.streamPromises;

		this.params = {
			channel: 2,
			kbps: 128
		}

		this.init();
	}

	init () {
		this.state = OFF;

		this.worker = new RecorderWorker();
		this.worker.onmessage = this.handleWorkerMessage.bind(this);

		this.getRecordingTool().then(this.setupRecording.bind(this));
	}

	/************* Controls *********************/

	on () {
		this.state = IDLE;
	}

	start () { 
		if (this.state == OFF || this.state == RECORDING) 
			return Promise.reject ("Error: Recording already started"); 

		this.state = RECORDING; 
		return Promise.resolve();
	}
	stop (showLoading) { 
		if (this.state == OFF || this.state == IDLE) 
			return Promise.reject("Error: Recording have yet started"); 

		// this.stream[0].end();
		// this.stream[1].end();
		if (showLoading)
			showLoading();

		this.state = IDLE; 

		return this.getAudioData("WAV"); 
	}

	/************* Actual Recording *********************/

	getMp3Data () {
		return this.requestAudioDataFromWorker("MP3");
	}

	getWavData () {
		return this.requestAudioDataFromWorker("WAV")
	}

	getAudioData (type) {
		if (type == "MP3")
			return this.getMp3Data ();
		else return this.getWavData ();
	}

	getRecordingTool () {
		return navigator.mediaDevices.getUserMedia({audio: true, video: false});
	}

	setupRecording (stream) {
		var ctx = new AudioContext();
		var source = ctx.createMediaStreamSource(stream);
		var gain = ctx.createGain();
		var scriptProcessor = ctx.createScriptProcessor(4096, 2, 2);

		this.params['sampleRate'] = ctx.sampleRate;
		this.initWorker ();

		scriptProcessor.onaudioprocess = this.handleOnAudioProcess.bind(this);

		source.connect(gain);
		gain.connect(scriptProcessor);
		scriptProcessor.connect(ctx.destination);
	}

	handleOnAudioProcess (ape) {
		if (this.state == OFF || this.state == IDLE) return;

		var inputBuffer = ape.inputBuffer;
		var outputBuffer = ape.outputBuffer;

		for (var channel = 0; channel < inputBuffer.numberOfChannels; channel++) {
			var inputData = inputBuffer.getChannelData (channel);
			var samples = [];

			for (var sample = 0; sample < inputData.length; sample++) {
				samples[sample] = inputData[sample];
			}

			this.handleSamples(samples, channel);
			
		}
	}

	handleSamples (samples, channel) {
		this.sendSamplesToWorker (samples, channel);
		// this.sendSamplesToServer (samples, channel);
	}

	/************* WORKER CONTROLLER *********************/

	initWorker () {
		// this.sendParamsToServer (channel, sampleRate, kbps);
		this.worker.postMessage ({
			command: "init"
		})
	}

	sendSamplesToWorker (samples, channel) {
		this.worker.postMessage ({
			command: "record",
			samples: samples,
			channel: channel
		})
	}

	requestAudioDataFromWorker (type) {
		this.worker.postMessage ({
			command: "process",
			type: type,
			params: this.params
		})
		return new Promise ((resolve, reject) => {
			this.workerPromise = function (audioData) {
				return resolve(audioData);
			}
		})
	}

	handleProcessedMp3 (mp3Data) {
		this.workerPromise (mp3Data);
	}

	// Function to handle messages returned from Worker
	printStatus (msg) {
		console.log ("Worker Message:\n\tCommand: " + msg.command + "\n\tStatus: " + msg.status);
	}
	handleWorkerMessage (e) {
		var msg = e.data;
		this.printStatus(msg);
		if (msg.status == 200) {
			switch (msg.command) {
				case "process": this.handleProcessedMp3 (msg.data);	break;
			}
		}
	}
}

module.exports = Recorder;