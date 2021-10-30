import discord
import warnings
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from Config import *

import zmq
import zmq.asyncio
import json

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Error supression for zmq

# Server block start
async def Init():
    sock = zmq.asyncio.Context().socket(zmq.REP)
    sock.bind(f"tcp://*:{INPORT}")
    while True:
        reply = await Process(json.loads(await sock.recv_string())) # Awaiting a message, loads it from json to list and sends to process
        await sock.send_string(reply)

async def Process(message):
    if (type(message) == list): # Expects a list type
        if (message[0] != SECRET): # If first variable does not match the SECRET key - respond with wrong key
            await ActionLog("Wrong key inputted.")
            return "Wrong key!"
        await ActionLog("Got a message from a node") # Else do something
        return "OK!"
    else: # If not a list type - respond with 418
        return "418 I'm a teapot"
# Server block end

# Bot preconfiguration
Triton=commands.Bot(command_prefix="<")

# This function sends a message to a specified logchannel in the config
async def ActionLog(message):
    if (LOGCHANNEL == 0):
        warnings.warn("LogChannel ID is not set!")
    else:
        await Triton.get_channel(LOGCHANNEL).send(message)

# Init event - starts when the bot is being booted up
@Triton.event
async def on_ready():
    print("Sadogire is running!")
    asyncio.get_event_loop().create_task(Init())
    await ActionLog("Triton instance launched.")

# Config checks before initialization 
def CheckConfig():
    if (TOKEN == ""): # If the token is empty - Assume Config.py was untouched
        raise ValueError("You have not configured the config file!\nPlease edit config.py with the required variables!")
    if (INPORT > 65535 or INPORT < 0): # If RFC 793 is violated - raise an error and explain why
        raise ValueError("Port value is incorrect! You are allowed to have a port number ranging from 1 to 65535 due to TCP header limitations! Negative numbers, 0, or anything over 65535 will not work!")
    if (OWNERID == 0): # If Owner is not specified - warn the user
        warnings.warn("OWNERID is not set! Sadogire cannot be used to its full extent without an owner!")
    if (LOGCHANNEL == 0): # If logchannel is not set - warn the user
        warnings.warn("LOGCHANNEL is not set! You will not receive log information via discord!")
    if (SECRET == "TwinklingStar"): # If the secret is default - warn the user
        warnings.warn("You are running Sadogire with the default secret! This is unsecure and may grant access to any third party!")

def Boot():
    CheckConfig()
    Triton.run(TOKEN)

Boot()