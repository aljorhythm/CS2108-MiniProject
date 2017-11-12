module.exports = function (target, audioData) {
    
    const audioEl = document.createElement('audio');
    audioEl.controls = true;
    const sourceEl = document.createElement('source');
    sourceEl.src = audioData;
    sourceEl.type = 'audio/wav';
    audioEl.appendChild(sourceEl);
    target.appendChild(audioEl);

    return audioEl;
}