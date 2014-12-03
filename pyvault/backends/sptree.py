#-*- coding: utf-8 -*-

import os
import json
import pairtree

from pyvault.backends import PyVaultBackend

class PyVaultShortenedPairtreeBackend(PyVaultBackend):
    """
        .. versionadded:: 0.2.2

        implements a flat file storage using pairtree with a maximum
        depth

        :param path: a filesystem path to store all data
                     under. metadata file is accessible as *.meta*.
        :param depth: the maximum depth of directories to create
                      under the pairtree root.
    """

    def __init__(self, path, depth=5):
        self._path = path
        self._depth = depth

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
        obj = self._store.get_object(key[:2*self._depth],
            create_if_doesnt_exist=True)
        if not obj.isfile(key):
            raise ValueError

        data = json.load(obj.get_bytestream(key, streamable=True))
        return data

    def store(self, key, data):
        obj = self._store.get_object(key[:2*self._depth],
            create_if_doesnt_exist=True)
        obj.add_bytestream(key, json.dumps(data))
