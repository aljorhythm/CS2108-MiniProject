module.exports = function (target, audioData) {
    
    return new Promise ((resolve, reject) => {
    	const audioEl = document.createElement('audio');
	    audioEl.controls = true;
	    const sourceEl = document.createElement('source');
	    sourceEl.src = audioData;
	    sourceEl.type = 'audio/wav';

	    audioEl.onloadeddata = () => {
	    	resolve(audioEl);
      }
      
      audioEl.onerror = (err) => {
        reject(err)
      }

	    audioEl.onloadstart = () => {
	    	console.log ("Loading!...", target);
	    }

	    audioEl.appendChild(sourceEl);
	    target.appendChild(audioEl);

	    audioEl.load();
    });
}