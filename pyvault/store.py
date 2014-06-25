#-*- coding: utf-8 -*-

import hashlib
import os
import os.path
import base64
import SecureString
import json

from pbkdf2 import PBKDF2
from pyvault.string import PyVaultString
from pyvault.utils import constant_time_compare
from pyvault.ciphers import cipher_manager

class PyVaultStore(object):
    def __init__(self, path, id):
        digest = hashlib.sha512(str(id)).hexdigest()
        self._file = os.path.join(path, digest)

    def retrieve(self, passphrase):
        def retrieve_key(data):
            key_salt = base64.b64decode(data['salt'])
            key_iv = base64.b64decode(data['iv'])
            key_derived = PBKDF2(passphrase, key_salt).read(32)
            message = cipher_manager.get(data['cipher']).decrypt(
                key_derived, key_iv, base64.b64decode(data['key'])
            )
            return (data['id'], message)

        with open(self._file, "r") as fp:
            data = json.load(fp)

        keys = dict([retrieve_key(x) for x in data['keys']])

        # decrypt payload
        pl_iv = base64.b64decode(data['payload']['iv'])
        payload = cipher_manager.get(data['payload']['cipher']).decrypt(
            keys[data['payload']['key']], pl_iv,
            base64.b64decode(data['payload']['data'])
        )
        pl_dg = hashlib.sha512(payload).hexdigest()

        # decrypt digest
        dg_iv = base64.b64decode(data['digest']['iv'])
        digest = cipher_manager.get(data['digest']['cipher']).decrypt(
            keys[data['digest']['key']], dg_iv,
            base64.b64decode(data['digest']['data'])
        )

        # compare digests
        compare = constant_time_compare(pl_dg, digest)

        # clean up memory
        map(lambda x: SecureString.clearmem(keys[x]), keys)
        if not compare:
            SecureString.clearmem(payload)

        return PyVaultString(payload)

    def store(self, passphrase, payload, cipher=None):
        def pad_payload(payload):
            pad_length = 16 - (len(str(payload)) % 16)
            pad = "".join('\x00' for x in xrange(0, pad_length))
            return str(payload) + pad

        # encryption key
        enc_salt = os.urandom(8) #64bit
        enc_iv = os.urandom(16) #128bit
        enc_dkey = PBKDF2(passphrase, enc_salt).read(32)
        enc_key = os.urandom(32)
        enc_data = cipher_manager.get(cipher).encrypt(
            enc_dkey, enc_iv, enc_key
        )

        # digest key
        dig_salt = os.urandom(8) #64bit
        dig_iv = os.urandom(16) #128bit
        dig_dkey = PBKDF2(passphrase, dig_salt).read(32)
        dig_key = os.urandom(32)
        dig_data = cipher_manager.get(cipher).encrypt(
            dig_dkey, dig_iv, dig_key
        )

        # encrypt payload
        padded_payload = pad_payload(payload)
        pl_iv = os.urandom(16) #128bit
        pl_data = cipher_manager.get(cipher).encrypt(
            enc_key, pl_iv, padded_payload
        )

        # create digest and encrypt
        dg_iv = os.urandom(16) #128bit
        dg_data = cipher_manager.get(cipher).encrypt(
            dig_key, dg_iv,
            hashlib.sha512(padded_payload).hexdigest()
        )

        # JSON object
        data = {
            'version': 1,
            'keys': [
                {'id': "encryption",
                 'salt': base64.b64encode(enc_salt),
                 'iv': base64.b64encode(enc_iv),
                 'cipher': cipher,
                 'key': base64.b64encode(enc_data)},
                {'id': "digest",
                 'salt': base64.b64encode(dig_salt),
                 'iv': base64.b64encode(dig_iv),
                 'cipher': cipher,
                 'key': base64.b64encode(dig_data)}
            ],
            'payload': {
                'key': "encryption",
                'iv': base64.b64encode(pl_iv),
                'cipher': cipher,
                'data': base64.b64encode(pl_data)
            },
            'digest': {
                'key': "digest",
                'iv': base64.b64encode(dg_iv),
                'cipher': cipher,
                'data': base64.b64encode(dg_data)
            }
        }

        with open(self._file, "w") as fp:
            fp.write(json.dumps(data))

        # clear up memory
        SecureString.clearmem(enc_salt)
        SecureString.clearmem(enc_iv)
        SecureString.clearmem(enc_key)
        SecureString.clearmem(dig_salt)
        SecureString.clearmem(dig_iv)
        SecureString.clearmem(dig_key)
        SecureString.clearmem(pl_iv)
        SecureString.clearmem(dg_iv)
        SecureString.clearmem(padded_payload)


