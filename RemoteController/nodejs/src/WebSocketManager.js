const rfr = require('rfr');
const WebSocket = require('ws');
const chalk = require('chalk');
const url = require('url');

class WebSocketManager {

    #server;
    #nightCrystal;
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
                            this.toNightCrystal(msg);

                            let jsonObj = JSON.parse(msg);
                        });
                    }

                    if(type == "nightCrystal") {

                        this.nightCrystal = ws;

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

    toNightCrystal(msg) {
        if(this.nightCrystal != null) {
            this.nightCrystal.send(msg);
        }
    }

}

module.exports = WebSocketManager;
