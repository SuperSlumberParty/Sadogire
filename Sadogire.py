#\x45\x4e\x44\x45\x52\x42\x4c\x49\x54\x5a\x27\x53\x0a
#\x53\x55\x50\x45\x52
#\x53\x4c\x55\x4d\x42\x45\x52
#\x50\x41\x52\x54\x59
import warnings
import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure

from Config import *
from SadogireObjects import *

import zmq # Communication via tcp
import zmq.asyncio

import json # Message enconding

from Util import Encryption

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Error supression for zmq

# Server block start
async def Init():
    sock = zmq.asyncio.Context().socket(zmq.REP)
    sock.setsockopt(zmq.SNDTIMEO, TIMEOUT)
    sock.bind(f"tcp://*:{INPORT}")
    while True:
        Request = await Encryption.Unscramble(await sock.recv(), SECRET)
        isSadoObject = await DetermineObject(Request)
        if (isSadoObject == False): # If Unknown - Deny
            await sock.send(b"You're delusional")
        else:
            Response = await Respond(Request)
            await sock.send(Response)
            


async def Respond(SadogireObject):
    return b"OK!"
    
async def DetermineObject(message):
    if (type(message) == Request or type(message) == NodeIdentity): # Checks for Request Object
        return True
    else:
        return False

# Bot preconfiguration
Triton=commands.Bot(command_prefix="<")

# This function sends a message to a specified logchannel in the config
async def ActionLog(message):
    if (LOGCHANNEL == 0):
        print(message) #Print error in console
    else:
        await Triton.get_channel(LOGCHANNEL).send(message)

# Init event - starts when the bot is being booted up
@Triton.event
async def on_ready():
    print("Sadogire is running!")
    asyncio.get_event_loop().create_task(Init())
    await ActionLog("Sadogire instance is running. Awaiting nodes")

# Config checks before initialization 
def CheckConfig():
    if (TOKEN == ""): # If the token is empty - Assume Config.py was untouched
        raise ValueError("You have not configured the config file!\nPlease edit config.py with the required variables!")
    if (INPORT > 65535 or INPORT < 0): # If RFC 793 is violated - raise an error and explain why
        raise ValueError("Port value is incorrect! You are allowed to have a port number ranging from 1 to 65535 due to TCP header limitations!\
                          Negative numbers, 0, or anything over 65535 will not work!")
    if (OWNERID == 0): # If Owner is not specified - warn the user
        warnings.warn("OWNERID is not set! Sadogire cannot be used to its full extent without an owner!")
    if (LOGCHANNEL == 0): # If logchannel is not set - warn the user
        warnings.warn("LOGCHANNEL is not set! You will not receive log information via discord!")
    if (SECRET == "TwinklingStar"): # If the secret is default - warn the user
        warnings.warn("You are running Sadogire with the default secret! This is unsecure and may grant access to any third party!")
    if (TIMEOUT > 3000): # If timeout is over 3 seconds - issue a warning
        warnings.warn("Timeout is too high! This may cause sadogire to malfunction!")



# Monkeypatch, monkeypatch
def warnformat(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'



def Boot():
    warnings.formatwarning = warnformat
    CheckConfig()
    Triton.run(TOKEN)

Boot()