import jwt

SECRET_AUTH_KEY = "d4594e98fe9461df13e047a39c8a1bcd6bfda5ed1ddb6c5fdc6d25d1479ed01dae670b84749b69166a51975b9201f64b7212f7d879391a415b12e497eff9fba85d7e5cefa4aa2c895c75d5de0684d7b23c80827c2ac4b1c242a47852156a4271e5e0bd2f261c359a405cc1ce118820ba7f834013d1c7cca24ea49e1e7d523e60"

import os

def generate_salt(key_length):
    return os.urandom(int(key_length/2)).hex()

print(len(jwt.encode({ "username": generate_salt(256), "type": "refresh", "device_id": 10**10 }, key=SECRET_AUTH_KEY, algorithm="HS512")))

print(jwt.decode(
    "d4594e98fe9461df13e047a39c8a1bcd6bfda5ed1ddb6c5fdc6d25d1479ed01dae670b84749b69166a51975b9201f64b7212f7d879391a415b12e497eff9fba85d7e5cefa4aa2c895c75d5de0684d7b23c80827c2ac4b1c242a47852156a4271e5e0bd2f261c359a405cc1ce118820ba7f834013d1c7cca24ea49e1e7d523e60",
    "d",
    algorithms=["HS512"]
))

