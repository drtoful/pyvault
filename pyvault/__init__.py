#-*- coding: utf-8 -*-

import os
from pyvault.meta import PyVaultMeta
from pyvault.string import PyVaultString

class PyVaultUnlockError(Exception):
    pass

class PyVault(object):
    def __init__(self, path):
        self._path = path
        self._meta = PyVaultMeta(os.path.join(path, ".meta"))
        self._locked = True
        self._masterkey = None

    def unlock(self, passphrase):
        if not self._meta.verify(passphrase):
            raise PyVaultUnlockError()

        self._locked = False
        self._masterkey = PyVaultString(passphrase)

    def lock(self):
        self._locked = True
        if not self._masterkey is None:
            self._masterkey.clear()
            self._masterkey = None

    def is_locked(self):
        return self._locked

    def get(self, id):
        pass

    def set(self, id, payload, cipher="default"):
        pass

    def create(self, passphrase):
        self._meta.create(passphrase)
