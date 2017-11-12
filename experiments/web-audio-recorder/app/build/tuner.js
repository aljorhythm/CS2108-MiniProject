const Recorder = require ("./Recorder/Recorder.js");
const S = require ("./Server/Server.js");

window.onload = function () {
	var R = new Recorder();
	var startBtn = document.getElementById("start");
	var stopBtn = document.getElementById("stop");
	var recordingText = document.getElementById("recording-status");
	var key = document.getElementById("key");

	var server = new S("127.0.0.1", "5000");

	R.on();
	startBtn.addEventListener("click", () => {
		recordingText.style.display = "inline-block";
		R.start();
	})
	stopBtn.addEventListener("click", ()=>{
		recordingText.style.display = "none";
		R.stop().then((blob) => {
			var reader = new FileReader();
			reader.readAsDataURL(blob);
			reader.addEventListener("load", () => {
				server.POST("/tuner", reader.result)
				.then((result) => {
					key.innerHTML = result.msg
				});
			})
		})
	})
}