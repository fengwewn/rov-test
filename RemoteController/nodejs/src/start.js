const rfr = require('rfr');
const chalk = require('chalk');
const http = require('http');
const express = require('express');
const readline = require('readline');

var app = express();
var server = http.createServer(app);

const WebSocketManagerClass = rfr('src/WebSocketManager.js');
const WebSocketManager = new WebSocketManagerClass(server);

server.listen(2915, '0.0.0.0', function() {

	var host = server.address().address;
	var port = server.address().port;

	console.log(chalk.green("Express ready at http://" + host + ":" + port));

	const rl = readline.createInterface({
	  input: process.stdin,
	  output: process.stdout
	});

	rl.setPrompt('> ');
	rl.prompt();
	rl.on('line', function(line) {

		var args = line.split(' ');
		var cmdlable =  args[0];
		for(var i=1; i<=args.length; i++) {
			args[i-1] = args[i];
			args.splice(args.length);
		}

		if(cmdlable == 'end') {
			rl.close();
		}

	    rl.prompt();
	}).on('close',function() {
	    process.exit(0);
	});

});

app.get('/', (req, res) => {
  res.send('Hello World!')
})
