const LameJs = require ("lameJs");
const RecorderWorker = require ("./Recorder.Worker.js");
const OFF = -1;
const RECORDING = 1;
const IDLE = 0;

class Recorder {
	constructor () {

		this.state;
		this.samples;
		this.mp3Encoder;
		this.mp3Data;

		this.init();
	}

	init () {
		this.state = OFF;
		this.samples = [];
		this.mp3Encoder = null;
		this.mp3Data = null;
		this.worker = new RecorderWorker();
		this.worker.onmessage = this.handleWorkerMessage.bind(this);
		this.getRecordingTool().then(this.setupRecording.bind(this));
	}

	on () {
		this.state = IDLE;
	}
	start () { 
		if (this.state == OFF) return; 
		this.state = RECORDING; 
	}
	stop () { 
		if (this.state == OFF) return; 
		this.state = IDLE; 
		
		return this.getMp3Data(); 
	}

	getMp3Data () {
		if (this.mp3Data == null) {
			return this.requestMp3DataFromWorker().then((mp3Data) => { 
				this.mp3Data = mp3Data;
				return this.getMp3Data();
			});
		} else return Promise.resolve(this.mp3Data);
	}

	processRecordedData () {

		var sampleBlockSize = 1152;
		var left = this.samples[0];
		var right = this.samples[1];

		var leftChunk, rightChunk, mp3buf;
		var mp3Data = [];

		return new Promise ((resolve, reject) => {
			for (var i = 0; i < left.length; i += sampleBlockSize) {
				leftChunk = left.subarray(i, i + sampleBlockSize);
				rightChunk = right.subarray(i, i + sampleBlockSize);
				mp3buf = this.mp3Encoder.encodeBuffer(leftChunk, rightChunk);
				if (mp3buf.length > 0) {
					mp3Data.push(mp3buf);
				}
			}
			mp3buf = this.mp3Encoder.flush();   //finish writing mp3

			if (mp3buf.length > 0) {
			    mp3Data.push(mp3buf);
			} else {
				reject ("No Buffered Data");
			}

			resolve(mp3Data);
		});
	}

	getRecordingTool () {
		return navigator.mediaDevices.getUserMedia({audio: true, video: false});
	}
	setupRecording (stream) {
		var ctx = new AudioContext();
		var source = ctx.createMediaStreamSource(stream);
		var gain = ctx.createGain();
		var scriptProcessor = ctx.createScriptProcessor(4096, 2, 2);

		this.sendParamsToWorker (2, ctx.sampleRate, 128);

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
				samples[sample] = inputData[sample] * 32767.5;
			}

			
			this.sendSamplesToWorker (samples, channel);
			
		}
	}

	sendParamsToWorker (channel, sampleRate, kbps) {
		this.worker.postMessage ({
			command: "init",
			params: {
				channels: channel,
				sampleRate: sampleRate,
				kbps: kbps
			}
		})
	}

	sendSamplesToWorker (samples, channel) {
		this.worker.postMessage ({
			command: "record",
			samples: samples,
			channel: channel
		})
	}

	requestMp3DataFromWorker () {
		
		this.worker.postMessage ({
			command: "process"
		})
		return new Promise ((resolve, reject) => {
			this.workerPromise = function (mp3Data) {
				return resolve(mp3Data);
			}
		})
	}

	handleProcessedMp3 (mp3Data) {
		this.workerPromise (mp3Data);
	}

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