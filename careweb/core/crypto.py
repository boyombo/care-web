import base64
import hashlib
import random

from Crypto.Cipher import AES
from django.conf import settings


def get_hash(order_id, amt, private_key):
    term = "{}{}{}{}{}".format(
        settings.PAYGATE_MERCHANT_ID, order_id, amt, "566", private_key
    )
    _term = term.encode("utf-8")
    _hash = hashlib.sha256(_term).digest()
    _str = base64.b64encode(_hash).decode("utf-8")
    return _str


class Encryptor:
    """
    A classical AES Cipher. Can use any size of data and any size of password thanks to padding.
    Also ensure the coherence and the type of the data with a unicode to byte converter.
    """

    def __init__(self):
        self.bs = 16
        self.key = hashlib.sha256(
            Encryptor.str_to_bytes(settings.PAYGATE_PUBLIC_KEY)
        ).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b"".decode("utf8"))
        if isinstance(data, u_type):
            return data.encode("utf8")
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * Encryptor.str_to_bytes(
            chr(self.bs - len(s) % self.bs)
        )

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]

    def generate_string(self, num_chars=16):
        code_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        code = ""
        for i in range(0, num_chars):
            slice_start = random.randint(0, len(code_chars) - 1)
            code += code_chars[slice_start : slice_start + 1]
        return code

    def encrypt(self, raw):
        raw = self._pad(Encryptor.str_to_bytes(raw))
        # iv = Random.new().read(AES.block_size)
        iv = settings.PAYGATE_PUBLIC_KEY.encode("utf-8")
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(cipher.encrypt(raw)).decode("utf-8")
        # return base64.b64encode(iv + cipher.encrypt(raw)).decode("utf-8")

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        # iv = enc[: AES.block_size]
        iv = settings.PAYGATE_PUBLIC_KEY.encode("utf-8")
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc)).decode("utf-8")
        # return self._unpad(cipher.decrypt(enc[AES.block_size :])).decode("utf-8")

    def get_encrypted_string(self, num_chars):
        the_string = self.generate_string(num_chars)
        encrypted = self.encrypt(the_string)
        return {"the_string": the_string, "encrypted": encrypted}
