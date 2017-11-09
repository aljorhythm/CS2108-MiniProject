let http = require ("http");

class Server {

	constructor (hostname, port) {
		this.options = {
			hostname: hostname,
			port: port
		}
	}

	parseUrlParams (params) {
		if (!params) return "";

		var query = "";
		var flag = false;
		var amp = "&";
		for (var key in params) {
			query += ((flag) ? "&" : "") + key + "=" + params[key];
			if (!flag) {
				flag = !flag;
			}
		}
		return query;
	}

	createRequest (option, resolve, reject) {
		var req = http.request(option, (res) => {
			var data = new Uint8Array();

			// Streaming Data In
			res.on('data', (chunk) => {

				var tmp = new Uint8Array(data.length + chunk.length);
				tmp.set(data);
				tmp.set(chunk, data.length)

				data = tmp;
			})

			// Stream Closed
			res.on('end', () => {
				resolve(data);
				console.log ("On End!");
			})
		})

		// Error
		req.on("error", (e) => {
			reject(e);
		})

		return req;
	}

	createPostOption (path, postData) {
		var option = this.createOption(path, "POST");
		if (postData) {
			option['headers'] = {
	    		'Content-Length': Buffer.byteLength(postData)
			}
		}
		return option;
	}

	createOption (path, method) {
		return Object.assign({
			path: path,
			method: method
		}, this.options);
	}

	makeHandleRes (isJSON) {
		return function (res) {
			if (!isJSON) {
				console.log ("NOT JSON!");
				return Promise.resolve(res);
			}

			res = new TextDecoder("utf-8").decode(res);
			try {
				var o = JSON.parse(res);
				if (o.status != 200)
					return Promise.reject(o);
				return Promise.resolve(o);
			} catch (e) {
				return Promise.resolve(res);
			}
		}
	}

	GET (path, params, isJSON=true) {

		// Set up get path
		path += '?' + this.parseUrlParams(params);
		var option = this.createOption(path, "GET");
		// Send GET request and return as a Promise
		return this.REQUEST (option, null, isJSON)
	}

	POST (path, postData, isJSON=true) {
		var option = this.createPostOption(path, postData);
		return this.REQUEST(option, postData, isJSON)
		
	}

	REQUEST (option, data, isJSON) {
		return new Promise ((resolve, reject) => {
			var req = this.createRequest(option, resolve, reject);
			if (data != null)
				req.write(data);
			req.end();
		})
		.then (this.makeHandleRes(isJSON).bind(this))
	}

}

module.exports = Server;