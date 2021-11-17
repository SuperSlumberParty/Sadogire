# Utility.Cryptography is responsible for Encoding&Encrypting and Decrypting&Decoding messages Sadogire sends and receives
# Encoding&Encrypting is called "Scramble", while Decrypting&Decoding is called "Unscramble"
# The algorhithm uses HKDF for Derision, which uses SECRET from Variables.Config

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import _get_backend, default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import base64
import pickle, zlib

from Variables.Config import SECRET



# Encrypts a message to be replied
async def Scramble(REP):
    Key = Fernet(await GetEncKey(SECRET))
    return Key.encrypt(zlib.compress(pickle.dumps(REP)))

# Unpacks a pickled compressed object into a readable SadogireObject
async def Unscramble(REQ):
    #        unpickles a decompressed Decrypted Object
    DecryptedREQ = await Decrypt(REQ, SECRET)
    if (DecryptedREQ == "Invalid Request"):
        return DecryptedREQ
    return pickle.loads(zlib.decompress(DecryptedREQ))

# Decrypts the message
async def Decrypt(Object, SECRET):
    try: # Attempt to decrypt object
        Key = Fernet(await GetEncKey(SECRET)) # Generate key
        DecryptedObj=Key.decrypt(Object) # Decrypt with said key
        return DecryptedObj # If no exceptions happen - return DecryptedObj
    except (cryptography.fernet.InvalidToken, TypeError): # If InvalidToken
        return "Invalid Request" # Return Invalid Request error to server function

# Retrieves an Encryption Key for Fernet
async def GetEncKey(SECRET):
    # Generate a BLAKE2b hash with a length of 32
    hkdf = HKDF(algorithm=hashes.BLAKE2b(64), length=32, 
                salt=None, info=None, backend=default_backend())
    #                      B64 Encode a derived hash with SECRET
    EncKey = base64.urlsafe_b64encode(hkdf.derive(SECRET.encode()))
    return EncKey