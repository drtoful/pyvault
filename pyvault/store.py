#-*- coding: utf-8 -*-

import hashlib
import os
import os.path
import base64
import SecureString
import json

from pyvault.string import PyVaultString
from pyvault.utils import constant_time_compare
from pyvault.ciphers import cipher_manager

class PyVaultStore(object):
    def __init__(self, backend, id):
        self._id = hashlib.sha512(str(id)).hexdigest()
        self._backend = backend

    def retrieve(self, passphrase):
        def retrieve_key(data):
            cipher = cipher_manager.get(data['cipher'])
            key_salt = base64.b64decode(data['salt'])
            key_iv = base64.b64decode(data['iv'])
            key_derived = cipher.derive_key(passphrase, key_salt)
            message = cipher.decrypt(
                key_derived, key_iv, base64.b64decode(data['key'])
            )
            return (data['id'], message)

        data = self._backend.retrieve(self._id)
        keys = dict([retrieve_key(x) for x in data['keys']])

        # decrypt payload
        pl_iv = base64.b64decode(data['payload']['iv'])
        payload = cipher_manager.get(data['payload']['cipher']).decrypt(
            keys[data['payload']['key']], pl_iv,
            base64.b64decode(data['payload']['data'])
        )
        pl_dg = hashlib.sha512(payload).hexdigest()

        # decrypt length
        length = None
        if not data['payload'].get('length', None) is None:
            length = cipher_manager.get(data['payload']['cipher']).decrypt(
                keys[data['payload']['key']], pl_iv,
                base64.b64decode(data['payload']['length'])
            )
            length = int(length.strip('\x00'))

        stored = payload
        if length is None:
            payload = stored.strip('\x00')
        else:
            payload = stored[:length]
        SecureString.clearmem(stored)

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

    def store(self, passphrase, payload, cipher=None, length=None):
        def pad_payload(payload):
            pad_length = 16 - (len(str(payload)) % 16)
            pad = "".join('\x00' for x in xrange(0, pad_length))
            return str(payload) + pad

        cipher = cipher_manager.get(cipher)
        if length is None:
            length = len(payload)

        # encryption key
        enc_salt = os.urandom(8) #64bit
        enc_iv = os.urandom(16) #128bit
        enc_dkey = cipher.derive_key(passphrase, enc_salt)
        enc_key = os.urandom(32)
        enc_data = cipher.encrypt(enc_dkey, enc_iv, enc_key)

        # digest key
        dig_salt = os.urandom(8) #64bit
        dig_iv = os.urandom(16) #128bit
        dig_dkey = cipher.derive_key(passphrase, dig_salt)
        dig_key = os.urandom(32)
        dig_data = cipher.encrypt(dig_dkey, dig_iv, dig_key)

        # encrypt payload
        padded_payload = pad_payload(payload)
        pl_iv = os.urandom(16) #128bit
        pl_data = cipher.encrypt(enc_key, pl_iv, padded_payload)

        padded_length = pad_payload(length)
        pl_length = cipher.encrypt(enc_key, pl_iv, padded_length)

        # create digest and encrypt
        dg_iv = os.urandom(16) #128bit
        dg_data = cipher.encrypt(
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
                 'cipher': cipher.id,
                 'key': base64.b64encode(enc_data)},
                {'id': "digest",
                 'salt': base64.b64encode(dig_salt),
                 'iv': base64.b64encode(dig_iv),
                 'cipher': cipher.id,
                 'key': base64.b64encode(dig_data)}
            ],
            'payload': {
                'key': "encryption",
                'iv': base64.b64encode(pl_iv),
                'cipher': cipher.id,
                'data': base64.b64encode(pl_data),
                'length': base64.b64encode(pl_length)
            },
            'digest': {
                'key': "digest",
                'iv': base64.b64encode(dg_iv),
                'cipher': cipher.id,
                'data': base64.b64encode(dg_data)
            }
        }

        self._backend.store(self._id, data)

        # clear up memory
        SecureString.clearmem(enc_salt)
        SecureString.clearmem(enc_iv)
        SecureString.clearmem(enc_key)
        SecureString.clearmem(dig_salt)
        SecureString.clearmem(dig_iv)
        SecureString.clearmem(dig_key)
        SecureString.clearmem(pl_iv)
        SecureString.clearmem(dg_iv)
        SecureString.clearmem(padded_length)
        if len(payload) % 16 > 0:
            SecureString.clearmem(padded_payload)
