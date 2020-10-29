# Dumb Remote Execution Agent
# Copyright © 2020 sinu <cpu344@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

import asyncio
import datetime
import json
import platform
import signal
import subprocess
import sys
import websockets

# --- Change here ---
pwd = 'password'
procpath = ['/path/to/process', '--arguments']
proccwd = None
port = 20003
# --- Change here ---

proc = None

psystem = platform.system()
if psystem != 'Linux' and psystem != 'Windows':
    print('This system is not supported.')
    sys.exit()

async def confunc(websocket, path):
    global psystem, pwd, proc, procpath, proccwd
    clientip = websocket.remote_address[0]

    print('Incoming connection from ' + clientip)

    try:
        if pwd != None:
            while (True):
                await websocket.send("pwd")
                pw = await websocket.recv()
                if pw == pwd:
                    print(clientip + ' sent correct password.')
                    await websocket.send("cmd")
                    break
                else:
                    print(clientip + ' sent wrong password.')
        else:
            await websocket.send("cmd")

        while (True):
            cmd = await websocket.recv()
            if cmd == "stat":                           # Process status (is it running?)
                print(clientip + ' requested process status check.')
                if proc is None:
                    await websocket.send("no")              # Process is not running.
                else:
                    await websocket.send("yes")             # Process is running.
            elif cmd == "run":                          # Start process
                # TODO: detect if process has been closed by itself?
                print(clientip + ' requested starting process.')
                if proc is None:
                    if proccwd is None:
                        proc = subprocess.Popen(procpath)
                    else:
                        proc = subprocess.Popen(procpath, cwd=proccwd)
                    await websocket.send("ok")              # Process has been started.
                else:
                    await websocket.send("ar")              # Process is already running.
            elif cmd == "stop":                         # Stop process
                print(clientip + ' requested stopping process.')
                if proc is None:
                    await websocket.send("nr")              # Process is not running.
                else:
                    if psystem == 'Linux':
                        proc.send_signal(signal.SIGINT)
                    else:
                        # is there any way to gracefully terminate process on windows?
                        proc.terminate()
                    proc.wait()
                    proc = None
                    await websocket.send("ok")              # Process has been stopped.
            elif cmd == "bye":                          # End connection
                print(clientip + ' requested closing connection.')
                await websocket.send("ok")
                await websocket.close()
                print(clientip + ' lost connection.')
                break
            else:
                print(clientip + ' requested unknown command(probably keep-alive).')
                await websocket.send("cmd")
    except websockets.ConnectionClosed:
        print(clientip + ' lost connection.')

start_server = websockets.serve(confunc, "0.0.0.0", port, close_timeout=300)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
