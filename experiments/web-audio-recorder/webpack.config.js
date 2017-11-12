const path = require ("path");
module.exports = [
	{
		entry: "./app/build/index.js",
		output: {
			path: path.resolve(__dirname, "./app/dist/"),
			filename: "webpack.bundle.js"
		},
		module: {
			rules : [
				{
			        test: /\.Worker\.js$/,
			        use: { 
			        	loader: 'worker-loader',
			        	options: { name: 'webWorker.worker.js' } 
			        }
			    }
			]
		}
	},

	{
		entry: "./app/build/tuner.js",
		output: {
			path: path.resolve(__dirname, "./app/dist/"),
			filename: "tuner.bundle.js"
		},
		module: {
			rules : [
				{
			        test: /\.Worker\.js$/,
			        use: { 
			        	loader: 'worker-loader',
			        	options: { name: 'webWorker.worker.js' } 
			        }
			    }
			]
		}
	},
]