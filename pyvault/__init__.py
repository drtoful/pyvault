#-*- coding: utf-8 -*-

import os
import SecureString

from pyvault.meta import PyVaultMeta
from pyvault.string import PyVaultString
from pyvault.store import PyVaultStore
from pbkdf2 import PBKDF2

class PyVaultUnlockError(Exception):
    pass

class PyVault(object):
    def __init__(self, path):
        self._path = path
        self._meta = PyVaultMeta(os.path.join(path, ".meta"))
        self._locked = True
        self._masterkey = None

    def unlock(self, passphrase, cleanup=True):
        self._locked = not self._meta.verify(passphrase)

        # derive masterkey from passphrase and salt
        # of vault (256bit key)
        self._masterkey = PyVaultString(
            PBKDF2(
                passphrase, self._meta.salt,
                iterations=self._meta.iterations
            ).read(64)
        )

        if cleanup:
            SecureString.clearmem(passphrase)

        if self.is_locked():
            raise PyVaultUnlockError()


    def lock(self):
        self._locked = True
        if not self._masterkey is None:
            self._masterkey.clear()
            self._masterkey = None

    def is_locked(self):
        return self._locked

    def retrieve(self, id):
        storage = PyVaultStore(self._path, id)
        return storage.retrieve(str(self._masterkey))

    def store(self, id, payload, cipher="default"):
        storage = PyVaultStore(self._path, id)
        storage.store(str(self._masterkey), payload)

    def create(self, passphrase, complexity=12, iterations=5000):
        self._meta.create(passphrase, complexity, iterations)
