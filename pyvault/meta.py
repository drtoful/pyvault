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
    def __init__(self, file):
        self.file = file
        self.salt = None
        self.iterations = None

    def verify(self, passphrase):
        if not os.path.isfile(self.file):
            return False

        try:
            with open(self.file, "r") as fp:
                data = json.load(fp)

            self.salt = base64.b64decode(data.get('salt'))
            self.iterations = data.get('iterations', 5000)
            return constant_time_compare(bcrypt.hashpw(
                passphrase.encode('utf-8'),
                data.get('passdigest').encode('utf-8')
            ), data.get('passdigest').encode('utf-8'))
        except ValueError:
            return False

    def create(self, passphrase, complexity=12, iterations=5000):
        if os.path.isfile(self.file):
            raise PyVaultMetaInitError()

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
            with open(self.file, "w") as fp:
                fp.write(json.dumps(object))
            os.chmod(self.file, 0600)
        except ValueError:
            raise PyVaultMetaInitError()

