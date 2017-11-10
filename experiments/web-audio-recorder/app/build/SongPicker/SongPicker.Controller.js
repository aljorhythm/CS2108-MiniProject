const SongPicker = require ("./SongPicker.js");
const Controller = require ("../Controller/Controller.js");
const AudioPlayer = require ("../Components/AudioPlayer/AudioPlayer.js");

class SongPickerController extends Controller {
	constructor (server, transposer) {
		super("songpicker");

		this.transposer = transposer;
		this.songpicker = new SongPicker(server);

		this.canSelectSong;
		this.playBtn;
		this.dommeta;

		this.initDom ();
	}

	start () {
		super.start();
		this.showDom();
	}

	initDom () {
		this.dommeta = {
			ul: {
				songlist: {
					type: "ul",
					classList: ["songlist"]
				}
			},
			li: {
				song: {
					type: "li",
					classList: ["song"]
				},

				title: {
					type: "p",
					classList: ["song-title", "song-info"]
				},

				author: {
					type: "p",
					classList: ["song-author", "song-info"]
				}
			}
		}
		this.canSelectSong = true;
		this.playBtn = document.getElementById("playbtn");
	}

	showDom () {
		var songlistDOM = document.getElementById("songlist");
		var ulDOM = this.createDOMs(this.dommeta.ul).songlist;

		this.startLoading("Fetching Song List...");
		this.songpicker.getSongList().then((songlist) => {
			this.stopLoading();
			for (var song in songlist) {
				this.addSongDom(ulDOM, songlist[song]);
			}
		})
		songlistDOM.appendChild(ulDOM);
	}

	addSongDom (songListDOM, song) {
		var songDOMs = this.createDOMs(this.dommeta.li);
		var songDOM = songDOMs.song,
			titleDOM = songDOMs.title,
			authorDOM = songDOMs.author;

		titleDOM.innerHTML = song.title;
		authorDOM.innerHTML = song.author;

		songDOM.appendChild(titleDOM);
		songDOM.appendChild(authorDOM);
		songDOM.addEventListener("click", this.makeHandleSongClick(song).bind(this));

		songListDOM.appendChild(songDOM);
	}

	makeHandleSongClick (song) {
		return () => {
			if (!this.canSelectSong) return;
			this.startLoading("Fetching Song...");
			this.songpicker.getSong(song).then((res) => {
				this.setPlayButton (song, res);
				this.stopLoading();
			});
		}
	}

	setPlayButton (song, res) {
		if (res == undefined) {
			console.log ("No Data!"); 
			return;
		}

		this.createAudioPlayer (this.playBtn, song, res);
	}

	createAudioPlayer (target, song, audioData) {
		var audioEl = AudioPlayer(target, audioData);
	    this.transposer.songpickerDone(song, audioEl);
	}

	startLoading (msg) {
		this.canSelectSong = false;
		this.transposer.loading(msg);
		console.log ("Start Loading");
	}

	stopLoading () {
		this.canSelectSong = true;
		this.transposer.loadend();
		console.log ("Stop Loading");
	}

}

module.exports = SongPickerController;