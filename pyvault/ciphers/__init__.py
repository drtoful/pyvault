#-*- coding: utf-8 -*-

class PyVaultCipher(object):
    def encrypt(self, key, iv, message):
        """
            Encrypt the given message securely.

            :param key: a session key which shall be used to
                        encrypt the message. The key is the result of
                        the `derive_key` method.
            :param iv: a initialization vector for block ciphers
            :return: a byte array (or string) containing the encrypted
                     message.
        """
        pass

    def decrypt(self, key, iv, message):
        """
            Decrypt a previously encrypt message.

            :param key: a session key which was used to encrypt
                        the message. The key is the result of the
                        `derive_key` method.
            :param iv: a initialization vector for block ciphers
            :return: a byte array (or string) containing the decrypted
                     message
        """
        pass

    def derive_key(self, passphrase, salt):
        """
            Derives a session key with the given passphrase and
            salt. This key is then used during encrypt and decrypt
            operations.

            Calling this method with the same passphrase and salt
            shall always yield the same key.

            :param passphrase: a byte array (or string) that contains
                               a secret from which to derive a session key
            :param salt: a byte array (or string) that contains a
                         random salt.
            :return: a byte array (or string) containing a session key
                     derived from passphrase and the salt.
        """
        pass

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
