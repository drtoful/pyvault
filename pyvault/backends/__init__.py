#-*- coding: utf-8 -*-

class PyVaultBackend(object):
    """Base class for all backend implementations"""

    def exists(self):
        """
            :return: True if the secure storage exists, False othersie
        """
        pass

    def create(self):
        """
            initializes the secure storage and creates necessary
            data. does not set the meta data for the secure storage.
        """
        pass

    def get_meta(self):
        """
            :returns: the meta dictionary for this secure storage
        """
        pass

    def set_meta(self, data):
        """
            sets the metadata information for this secure storage.
            Should only be called once (when creating a new secure
            storage).

            :param data: a meta dictionary

            :raises: :py:class:`ValueError`
        """
        pass

    def retrieve(self, key):
        """
            :param key: sha512 hexdigest
            :returns: a dictionary previously stored under the same
                      key

            :raises: :py:class:`ValueError`
        """
        pass

    def store(self, key, data):
        """
            :param key: sha512 hexdigest
            :param data: dictionary

            :raises: :py:class:`ValueError`
        """
        pass
