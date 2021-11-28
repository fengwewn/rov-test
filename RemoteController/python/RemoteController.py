import asyncio
import websockets
import json
import time

class RemoteController:

    def __init__(self, TimedController):
        self.tc = TimedController
        self.lc = self.tc.LowController
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.startWs())

    def processMsg(self, msg):
        print(msg)
        jsonObj = json.loads(msg)

        if jsonObj["action"] == "updateJoyStick":
            if jsonObj["stick"] == "turn":
                data = jsonObj["data"]
                if data > 0:
                    if data > 100: data = 100
                    self.lc.rotateClockwise(data)
                elif data < 0:
                    if data < -100: data = -100
                    self.lc.rotateAntiClockwise(-data)
                else:
                    self.lc.stop()
            elif jsonObj["stick"] == "forward":
                data = jsonObj["data"]
                if data > 0:
                    if data > 100: data = 100
                    self.lc.forwards(data)
                elif data < 0:
                    if data < -100: data = -100
                    self.lc.backwards(-data)
                else:
                    self.lc.stop()
        
        if jsonObj["action"] == "updateObjShipper":
            self.lc.moveLifter(jsonObj["data"])

    async def startWs(self):
        uri = "wss://sites.google.com/view/juneer2021fall/websocket/?type=project_haws"
        async with websockets.connect(uri) as websocket:
            while True:
                msg = await websocket.recv()
                self.processMsg(msg)
