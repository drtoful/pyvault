#-*- coding: utf-8 -*-

from pyvault.backends import PyVaultBackend
from pymongo import MongoClient

class PyVaultMongoBackend(PyVaultBackend):
    def __init__(self, uri):
        self._db = MongoClient(uri)
        if isinstance(self._db, MongoClient):
            dbname = (uri.rsplit("/", 1)[1]).split("?", 1)[0]
            self._db = getattr(self._db, dbname)

        self._db.store.ensure_index("id", background=True)

    def create(self):
        pass

    def get_meta(self):
        meta = self._db.store.find_one({"id": "_meta"})
        if meta is None:
            raise ValueError

        return meta

    def set_meta(self, data):
        meta = self._db.store.find_one({"id": "_meta"})
        if not meta is None:
            raise ValueError

        data['id'] = "_meta"
        self._db.store.insert(data)

    def retrieve(self, key):
        item = self._db.store.find_one({"id": key})
        if item is None:
            raise ValueError

        return item

    def store(self, key, data):
        data['id'] = key
        self._db.store.update(
            spec={"id": key},
            document=data,
            upsert=True
        )

