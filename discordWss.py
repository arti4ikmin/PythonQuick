# Python File used for arti-core, aswell as arti-tracker, CHECK LICENSE OF THE PROJECTS IN CASE THIS IS USED FOR COMMERCIAL PURPOSES.

import asyncio
import json
import websockets
from queue import Queue
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

data_queue = Queue()

def load_config():
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
            token = config.get("discordTrackingToken")
            tracking_username = config.get("discordTrackingUsername")
            return token, tracking_username
    except FileNotFoundError:
        print("err: config.json file not found")
    except json.JSONDecodeError:
        print("err: config.json file is not in valid josn format")
    return None, None

async def send_json_request(ws, request):
    await ws.send(json.dumps(request))

async def receive_json_response(ws):
    response = await ws.recv()
    if response:
        return json.loads(response)

async def heartbeat(interval, ws):
    print("Heartbeat started")
    try:
        while True:
            await asyncio.sleep(interval)
            heartbeat_json = {"op": 1, "d": None}
            await send_json_request(ws, heartbeat_json)
            print("Hearthbeat sent")
    except asyncio.CancelledError:
        print("Hearthbeat task cancelled")
    except Exception as e:
        print(f"Hearthbeat err: {e}")

async def startwss(token, tracking_username):
    uri = 'wss://gateway.discord.gg/?v=10&encoding=json'
    
    while True:
        try:
            async with websockets.connect(uri) as ws:
                event = await receive_json_response(ws)
                heartbeat_interval = event['d']['heartbeat_interval'] / 1000

                asyncio.create_task(heartbeat(heartbeat_interval, ws))

                payload = {
                    'op': 2,
                    "d": {
                        "token": token,
                        "properties": {
                            "$os": "windows",
                            "$browser": "chrome",
                            "$device": 'pc'
                        }
                    }
                }

                await send_json_request(ws, payload)

                while True:
                    try:
                        event = await receive_json_response(ws)

                        if event.get('op') == 11:
                            print("Heartbeat ACK received")

                        if 'd' in event and 'author' in event['d']:
                            username = event['d']['author']['username']
                            content = event['d']['content']
                            #print(f"{username}: {content}")

                            if username == tracking_username:
                                data_queue.put(event)
                    except websockets.ConnectionClosed as e:
                        print(f"Wss connection closed: {e}")
                        break
                    except Exception as e:
                        print(f"err while processing message: {e}")

        except Exception as e:
            print(f"Wss connection error: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)

async def send_data(websocket):
    while True:
        if not data_queue.empty():
            data = data_queue.get()
            await websocket.send(json.dumps(data))
            print(f"forwarded data: {data}")
        await asyncio.sleep(0.3)

async def main():
    token, tracking_username = load_config()
    if not token or not tracking_username:
        print("err: can not load token or tracking username from cfg")
        return

    asyncio.create_task(startwss(token, tracking_username))

    server = await websockets.serve(send_data, "localhost", 8765)
    print("Local Wss server started on ws://localhost:8765")

    try:
        await server.wait_closed()
    except asyncio.CancelledError:
        print("Server closed.")
        await server.close()

if __name__ == "__main__":
    asyncio.run(main())
