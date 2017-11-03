const LameJs = require ("lameJs");
var mp3Encoder,
	samples;

function init (params) {
	mp3Encoder = new LameJs.Mp3Encoder (params.channels, params.sampleRate, params.kbps);
	samples = [new Float32Array(), new Float32Array()];

	self.postMessage ({command: "init", status: 200});
} 

function record (_samples, _channel) {
	_samples = new Float32Array (_samples);
	var tmp = new Float32Array (samples[_channel].length + _samples.length);
	tmp.set(samples[_channel]);
	tmp.set(_samples, samples[_channel].length);
	samples[_channel] = tmp;

	self.postMessage ({command: "record", status: 200});
}

function process () {
	var sampleBlockSize = 1152;
	var left = samples[0];
	var right = samples[1];

	var leftChunk, rightChunk, mp3buf;
	var mp3Data = [];

	for (var i = 0; i < left.length; i += sampleBlockSize) {
		leftChunk = left.subarray(i, i + sampleBlockSize);
		rightChunk = right.subarray(i, i + sampleBlockSize);
		mp3buf = mp3Encoder.encodeBuffer(leftChunk, rightChunk);
		if (mp3buf.length > 0) {
			mp3Data.push(mp3buf);
		}
	}
	mp3buf = mp3Encoder.flush();   //finish writing mp3

	if (mp3buf.length > 0) {
	    mp3Data.push(mp3buf);
	} else {
		reject ("No Buffered Data");
	}

	self.postMessage ({command: "process", status: 200, data: mp3Data});
}

self.onmessage = function (event) {
	console.log(event);
	var data = event.data;
	switch (data.command) {
		case "init"  	: init (data.params); 					break; 
		case "record"	: record (data.samples, data.channel); 	break;
		case "process" 	: process ();							break;
	}
}