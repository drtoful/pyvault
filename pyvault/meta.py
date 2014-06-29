#-*- coding: utf-8 -*-

import bcrypt
import json
import os
import os.path
import base64
import SecureString

from pyvault.utils import constant_time_compare

class PyVaultMetaInitError(Exception):
    pass

class PyVaultMeta(object):
    def __init__(self, backend):
        self._backend = backend
        self.salt = None
        self.iterations = None

    def verify(self, passphrase):
        try:
            data = self._backend.get_meta()
            self.salt = base64.b64decode(data.get('salt'))
            self.iterations = data.get('iterations', 5000)

            return constant_time_compare(bcrypt.hashpw(
                passphrase.encode('utf-8'),
                data.get('passdigest').encode('utf-8')
            ), data.get('passdigest').encode('utf-8'))
        except ValueError:
            return False

    def create(self, passphrase, complexity=12, iterations=5000):
        object = dict(
            version = 1,
            salt = base64.b64encode(os.urandom(8)),  #64bit salt
            iterations = iterations,
            passdigest = bcrypt.hashpw(
                passphrase.encode('utf-8'),
                bcrypt.gensalt(complexity)
            )
        )

        try:
            self._backend.create()
            self._backend.set_meta(object)
        except ValueError:
            raise PyVaultMetaInitError()

