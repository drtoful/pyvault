#-*- coding: utf-8 -*-

import os
import json

from pyvault.backends import PyVaultBackend

class PyVaultFileBackend(PyVaultBackend):
    def __init__(self, path):
        self._path = path

    def create(self):
        try:
            os.makedirs(self._path, 0700)
        except OSError:
            pass

    def set_meta(self, data):
        file = os.path.join(self._path, ".meta")

        if os.path.isfile(file):
            raise ValueError

        with open(file, "w") as fp:
            json.dump(data, fp)

        os.chmod(file, 0600)

    def get_meta(self):
        file = os.path.join(self._path, ".meta")
        if not os.path.isfile(file):
            raise ValueError

        with open(file, "r") as fp:
            data = json.load(fp)

        return data

    def retrieve(self, key):
        file = os.path.join(self._path, key)
        if not os.path.isfile(file):
            raise ValueError

        with open(file, "r") as fp:
            data = json.load(fp)

        return data

    def store(self, key, data):
        file = os.path.join(self._path, key)

        with open(file, "w") as fp:
            data = json.dump(data, fp)

        os.chmod(file, 0600)

