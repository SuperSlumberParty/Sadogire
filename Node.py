import zmq, zlib, pickle, base64 # Client
from SadogireObjects import RequestObject
from Config import SECRET, INPORT

# Cryptography
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import _get_backend, default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

flags=0
protocol=-1
ObjObj=RequestObject(0,"Misfortune")
hkdf = HKDF(algorithm=hashes.SHA256(), length=32, 
                salt=None, info=None, backend=default_backend())
EncKey = base64.urlsafe_b64encode(hkdf.derive(SECRET.encode()))
Key = Fernet(EncKey)

Payload = Key.encrypt(zlib.compress(pickle.dumps(ObjObj)))

sock = zmq.Context().socket(zmq.REQ)
sock.connect(f"tcp://127.0.0.1:{INPORT}")
sock.send(Payload)
print("sent!")
print(sock.recv())