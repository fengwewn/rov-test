const rfr = require('rfr');
const WebSocket = require('ws');
const chalk = require('chalk');
const url = require('url');

class WebSocketManager {

    #server;
    #proJectHAWS;
    #controllers;
    constructor(server) {
        this.server = server;
        this.controllers = [];

        this.startListenWebSocket();
    }

    startListenWebSocket() {

        this.server.on('upgrade', (request, socket, head) => {

            let url = request.url;
            console.log('WebSocket attempt at ' + url);
            let res = url.match('\\/websocket\\/\\?(.*)');

            if(res != null) {

                let paramsStr = res[1];
                let searchParams = new URLSearchParams(paramsStr);
                // console.log(searchParams);

                let type = searchParams.get('type');

                //Define socket usage
                const wss = new WebSocket.Server({ noServer: true });

                wss.on('connection', (ws, request) => {
                    console.log("WS CONN: " + request.socket.remoteAddress + "(" + type + ")");

                    //subscriber.ws = ws;

                    if(type == "controller") {

                        this.controllers.push(ws);

                        ws.on('message', (msg) => {
                            //this.processMessage(subscriber, msg);
                            console.log("REV: " + msg);
                            this.toProJectHAWS(msg);

                            let jsonObj = JSON.parse(msg);
                        });
                    }

                    if(type == "project_haws") {

                        this.proJectHAWS = ws;

                    }
                });

                wss.handleUpgrade(request, socket, head, function done(ws) {
                    wss.emit('connection', ws, request);
                });

            }else {
                socket.destroy();
            }

        });

    }

    toProJectHAWS(msg) {
        if(this.proJectHAWS != null) {
            this.proJectHAWS.send(msg);
        }
    }

}

module.exports = WebSocketManager;
