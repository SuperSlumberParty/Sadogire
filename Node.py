import zmq, zlib, pickle, base64

from SadogireObjects import Request
from Config import SECRET, INPORT

# Cryptography
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import _get_backend, default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# Filler RequestObject object
ObjObj=Request(0,"Misfortune") 

# Generate a simple HKDF object using BLAKE2b hashing
hkdf = HKDF(algorithm=hashes.BLAKE2b(64), length=32, 
                salt=None, info=None, backend=default_backend())
#                  Base64 encode a HKDF derived SECRET(bytes of)
EncKey = base64.urlsafe_b64encode(hkdf.derive(SECRET.encode()))
# Generate Key based on EncKey
Key = Fernet(EncKey)

#             Encrypt a zip compressed  pickled  object
Payload = Key.encrypt(zlib.compress(pickle.dumps(ObjObj)))

# 
sock = zmq.Context().socket(zmq.REQ)
sock.connect(f"tcp://127.0.0.1:{INPORT}")
sock.send(Payload)
print("sent!")
print(sock.recv())