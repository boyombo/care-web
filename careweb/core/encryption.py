import base64
from Crypto import Random
from Crypto.Cipher import AES
import os
import time


class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        bt = base64.b64decode(s)
        return bt + b"\0" * (AES.block_size - len(bt) % AES.block_size)

    def encrypt(self, message):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)
