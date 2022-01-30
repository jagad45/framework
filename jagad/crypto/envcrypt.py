import zlib
import base64
import json

def encrypt_data(data):
    jsndump = json.dumps(data)
    encoder = base64.b32encode(jsndump.encode())
    return zlib.compress(encoder)

def decrypt_data(data):
    if isinstance(data, str):
        data = bytes(data)

    try:
        zlib_decoder = zlib.decompress(data)
        decoder = base64.b32decode(zlib_decoder)
        return json.loads(decoder)
    except Exception:
        return False