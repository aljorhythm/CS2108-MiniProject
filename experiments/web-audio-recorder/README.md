# Web Audio Recorder

## Idea

`navigator.mediaDevices.getUserMedia` 
	--> `AudioContext.createMediaStreamSource` 
		--> `AudioContext.createScriptProcessor` 
			--> `LameJs` (Web worker)
				--> `Mp3`

## Usage

```
	npm install
	npm run start:dev
```