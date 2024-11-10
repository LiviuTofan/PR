import asyncio
import websockets
import json

connected_users = set()

async def websocket_handler(websocket, path):
    username = None
    try:
        async for message in websocket:
            data = json.loads(message)
            print(data)
            if data["command"] == "join_room":
                username = data["username"]
                connected_users.add(websocket)
                await broadcast(f"{username} has joined the chat!")

            elif data["command"] == "send_msg":
                msg = f"{username}: {data['message']}"
                await broadcast(msg)

            elif data["command"] == "leave_room":
                await websocket.close()
    except websockets.ConnectionClosed:
        print(f"Connection with {username} closed.")
        pass
    finally:
        if websocket in connected_users:
            connected_users.remove(websocket)
            if username:
                await broadcast(f"{username} has left the chat.")

async def broadcast(message):
    for user in connected_users:
        try:
            await user.send(message)
        except websockets.ConnectionClosed:
            pass

def start_websocket_server():
    # Create a new event loop for the WebSocket server so it doesn't interfere with Flask's event loop
    asyncio.set_event_loop(asyncio.new_event_loop())
    port = 6800
    # Start the WebSocket server and listen for incoming connections calling the handler function
    start_server = websockets.serve(websocket_handler, "0.0.0.0", port)
    
    try:
        # Start the WebSocket server within the new event loop created above
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except OSError as e:
        if e.errno == 98:
            print(f"Port {port} is already in use. Please ensure no other instances are running.")
        else:
            print(f"An error occurred: {e}")
