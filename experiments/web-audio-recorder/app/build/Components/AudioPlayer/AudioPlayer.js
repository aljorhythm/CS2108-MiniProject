module.exports = function (target, audioData) {
	var blob = new Blob([audioData], {type:"audio/wav"});
	var url = window.URL.createObjectURL(blob);
	
	const audioEl = document.createElement('audio');
    audioEl.controls = true;
    const sourceEl = document.createElement('source');
    sourceEl.src = url;
    sourceEl.type = 'audio/wav';
    audioEl.appendChild(sourceEl);
    target.appendChild(audioEl);

    return audioEl;
}