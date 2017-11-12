const S = require("../Server/Server.js");
class SongPicker {
	constructor (server) {
		this.available;
		this.server = server
		this.initAvailable();
	}

	initAvailable () {
		
	}

	getSongList () {
		if (this.available == null) {
			return this.requestSongList();
		} else return Promise.resolve (this.available);
	}

	requestSongList () {
		return this.server.GET("/songlist").then((res) => {
			var songlist = res.msg;
			this.available = songlist;
			return Promise.resolve(this.available);
		})
	}

	getSong (song) {
		return this.requestSong (song);
	}

	requestSong (song) {
		var url = encodeURI("/songlist/" + song.title + "/" + song.author);
		if (song.author.length < 1)
			url = encodeURI("/songlist/" + song.title);
		

		return this.server.GET(url, null)
		.catch((err) => {
			console.log ("Error: " + err.msg);
		})
	}
}

module.exports = SongPicker;