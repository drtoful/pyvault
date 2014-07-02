#-*- coding: utf-8 -*-

from Crypto.Cipher import AES

class PyVaultCipherAES(object):
    """
        Implements AES cipher in CBC mode using a 256bit key.
    """

    def __init__(self):
        pass

    def encrypt(self, key, iv, message):
        c = AES.new(key, AES.MODE_CBC, iv)
        return c.encrypt(message)

    def decrypt(self, key, iv, message):
        c = AES.new(key, AES.MODE_CBC, iv)
        return c.decrypt(message)
