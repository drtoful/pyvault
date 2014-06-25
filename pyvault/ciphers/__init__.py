#-*- coding: utf-8 -*-

class PyVaultUnknownCipher(Exception):
    pass

class _PyVaultCiphers(object):
    def __init__(self):
        self._ciphers = {}

        try:
            from pyvault.ciphers.aes import PyVaultCipherAES

            cipher = PyVaultCipherAES()
            self._ciphers["aes"] = cipher
            self._ciphers["aes_cbc"] = cipher
        except:
            pass

    def get(self, cipher=None):
        if cipher is None:
            cipher = "aes" # default cipher

        c = self._ciphers.get(cipher.lower(), None)
        if c is None:
            raise PyVaultUnknownCipher(cipher)
        return c


cipher_manager = _PyVaultCiphers()
