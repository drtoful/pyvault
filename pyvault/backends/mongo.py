#-*- coding: utf-8 -*-

from pyvault.backends import PyVaultBackend
from pymongo import MongoClient

class PyVaultMongoBackend(PyVaultBackend):
    """
        implements a MonoDB backend

        :param uri: a MongoURI that selects the database
                    to store all data under.
        :param collection: select the collection to save the
                           data under
    """

    def __init__(self, uri, collection='store'):
        self._db = MongoClient(uri)
        if isinstance(self._db, MongoClient):
            dbname = (uri.rsplit("/", 1)[1]).split("?", 1)[0]
            self._db = getattr(self._db, dbname)

        self._db = getattr(self._db, collection)
        self._db.ensure_index("id", background=True)

    def exists(self):
        meta = self._db.find_one({"id": "_meta"})
        return not meta is None

    def create(self):
        pass

    def get_meta(self):
        meta = self._db.find_one({"id": "_meta"})
        if meta is None:
            raise ValueError

        return meta

    def set_meta(self, data):
        meta = self._db.find_one({"id": "_meta"})
        if not meta is None:
            raise ValueError

        data['id'] = "_meta"
        self._db.insert(data)

    def retrieve(self, key):
        item = self._db.find_one({"id": key})
        if item is None:
            raise ValueError

        return item

    def store(self, key, data):
        data['id'] = key
        self._db.update(
            spec={"id": key},
            document=data,
            upsert=True
        )

