const Loading = require ("../Components/Loading/Loading.js");
class Controller {
	constructor (target) {

		this.current = false;
		if (target != null)
			this.target = document.getElementById(target);
		this.doms = {}
	}

	start () {
		if (this.current) {
			return console.log ("[Controller]: Already Started!");
		} 
		this.current = true;
		this.target.classList.add("current");
	}

	stop () {
		if (!this.current) {
			return console.log ("[Controller]: Not Started!");
		}
		this.current = false;
		this.target.classList.remove("current");
	}

	createDOMs (doms) {
		var result = {};
		var domInfo, dom;
		for (var id in doms) {
			domInfo = doms[id];
			dom = document.createElement(domInfo.type);
			dom.className = domInfo.classList.join(" ");
			result[id] = dom;
		}
		return result;
	}

	getButton (id, onClick) {
		var btn = document.getElementById(id);
		btn.addEventListener ("click", onClick.bind(this));
		return btn;
	}

	setInnerHTML(id, value) {
		if (this.doms[id])
			return this.doms[id].innerHTML = value;
		var dom = document.getElementById(id);
		dom.innerHTML = value;
	}
}

module.exports = Controller