#-*- coding: utf-8 -*-

import os
import json
import pairtree

from pyvault.backends import PyVaultBackend

class PyVaultPairtreeBackend(PyVaultBackend):
    """
        implements a flat file storage using pairtree

        :param path: a filesystem path to store all data
                     under. metadata file is accessible as *.meta*.
    """

    def __init__(self, path):
        self._path = path

        f = pairtree.PairtreeStorageFactory()
        self._store = f.get_store(store_dir=self._path, uri_base="pyvault:/")

    def exists(self):
        file = os.path.join(self._path, ".meta")
        return os.path.isfile(file)

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
        obj = self._store.get_object(key, create_if_doesnt_exist=True)
        if not obj.isfile("data"):
            raise ValueError

        data = json.load(obj.get_bytestream("data", streamable=True))
        return data

    def store(self, key, data):
        obj = self._store.get_object(key, create_if_doesnt_exist=True)
        obj.add_bytestream("data", json.dumps(data))
