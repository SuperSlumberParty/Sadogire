import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from Config import *

import zmq
import zmq.asyncio
import json

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Error supression

# Server block start
async def Init():
    sock = zmq.asyncio.Context().socket(zmq.REP)
    sock.bind(f"tcp://*:{INPORT}")
    while True:
        reply = await Process(json.loads(await sock.recv_string()))
        await sock.send_string(reply)

async def Process(message):
    if (type(message) == list):
        if (message[0] != SECRET):
            await ActionLog("Wrong key inputted.")
            return "Wrong key!"
        await ActionLog("Got a message from a node")
        return "OK!"
    else:
        return "418 I'm a teapot"
# Server block end

# Bot preconfiguration
Triton=commands.Bot(command_prefix="<")

async def ActionLog(message):
    await Triton.get_channel(LOGCHANNEL).send(message)

# Init event - starts when the bot is being booted up
@Triton.event
async def on_ready():
    print("Sadogire is running!")
    asyncio.get_event_loop().create_task(Init())
    await ActionLog("Triton instance launched.")


def Boot():
    if (TOKEN == ""):
        print("You have not configured the config file!\nPlease edit config.py with the required variables!")
        exit(0)
    else:
        if (SECRET == "TwinklingStar"):
            print("You are running Sadogire with the default secret! This is unsecure and may grant access to any third party!")
        Triton.run(TOKEN)

Boot()