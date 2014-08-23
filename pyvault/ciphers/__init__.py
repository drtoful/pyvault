#-*- coding: utf-8 -*-

class PyVaultUnknownCipher(Exception):
    pass

class _PyVaultCiphers(object):
    def __init__(self):
        self._ciphers = {}

    def register(self, id, obj):
        self._ciphers[id] = obj

    def get(self, cipher=None):
        if cipher is None:
            cipher = "aes" # default cipher

        c = self._ciphers.get(cipher.lower(), None)
        if c is None:
            raise PyVaultUnknownCipher(cipher)
        return c

cipher_manager = _PyVaultCiphers()

try:
    from pyvault.ciphers.aes import PyVaultCipherAES

    cipher = PyVaultCipherAES()
    cipher_manager.register("aes", cipher)
    cipher_manager.register("aes-cbc", cipher)
except:
    pass
