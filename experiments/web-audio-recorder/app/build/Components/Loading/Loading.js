class Loading {
	constructor (target, size=1) {
		this.target = document.getElementById(target);
		this.target.style.display = "none"

		this.interval;
		this.NO_OF_BARS = 8;
		this.bars = [];
		this.Y_GROWTH = 15 * size;
		this.HEIGHT = 40 * size;
		this.TOP = (this.target.parentNode.clientHeight) 
			? (this.target.parentNode.clientHeight - this.HEIGHT) / 2 - this.HEIGHT
			: 0;
		this.LOADING = "Loading...";

		var margin = 2;
		var padding = 20;
		var width = (window.innerWidth - (this.NO_OF_BARS * margin * 2) - (padding * 2)) / this.NO_OF_BARS;
		var max_width = 10;
		this.WIDTH = ((width > max_width) ? max_width : width) * size;
		var offsettop = this.TOP;
		for (var i = 0; i < this.NO_OF_BARS; i++) {
			var bar = document.createElement("div");
			bar.classList.add ("loading-bar");
			bar.style.width = this.WIDTH + "px";
			bar.style.height = this.HEIGHT + "px";
			bar.style.marginLeft = margin + "px";
			bar.style.marginRight = margin + "px"; 
			bar.style.top = offsettop + "px";
			this.bars.push(bar);
			this.target.appendChild(bar);
		}

		this.message = document.createElement("div");
		this.message.id = "loading-msg";
		this.message.innerHTML = this.LOADING;
		if (this.TOP > 0)
			this.message.style.top = this.TOP - padding + "px";
		this.target.appendChild(this.message);
	}

	show (msg) {
		this.hide();


		this.message.innerHTML = msg || this.LOADING;
		var arr = [0,1,2,3,4,5,6,7];
		var dy = [0,1,2,1,0,-1,-2,-1];
		this.interval = setInterval(() => {

			this.target.style.display = "block"
			var i, yy, xx, h, bar;
			for (i = 0; i < arr.length; i++) {
				yy = this.HEIGHT + dy[i] * this.Y_GROWTH;
				h = this.TOP + ((yy + this.HEIGHT) / 2);
				bar = this.bars[arr[i]];
				bar.style.top = h + "px";
			}
			for (i = 0; i < arr.length; i++) {
				arr[i] = (arr[i] + 1) % this.NO_OF_BARS;
			}
		}, 100);

		this.target.classList.add("show");
	}

	hide () {
		if (!this.interval) return;

		this.target.style.display = "none"
		clearInterval(this.interval);
		this.target.classList.remove("show");
	}
}

module.exports = Loading;