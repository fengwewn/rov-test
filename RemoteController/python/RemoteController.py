import asyncio
import websockets
import json

def processMsg(msg):
    jsonObj = json.loads(msg)

    if jsonObj["action"] == "updateJoyStick":
        if jsonObj["stick"] == "turn":
            print("Turn: " + str(jsonObj["data"]))
        elif jsonObj["stick"] == "forward":
            print("Forward: " + str(jsonObj["data"]))

async def hello():
    uri = "wss://sites.google.com/view/juneer2021fall/websocket/?type=nightCrystal"
    async with websockets.connect(uri) as websocket:
        while True:
            msg = await websocket.recv()
            processMsg(msg)

loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
