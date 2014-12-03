#-*- coding: utf-8 -*-

import os
import SecureString

from pyvault.meta import PyVaultMeta
from pyvault.string import PyVaultString
from pyvault.store import PyVaultStore
from pbkdf2 import PBKDF2

class PyVaultUnlockError(Exception):
    """
    """
    pass

class PyVault(object):
    """
        This class represents a encrypted storage. All data within this
        storage is encrypted and can only be accessed, when the correct
        passphrase is provided.

        You can choose between different backends and ciphers to
        fullfill your requirements of security.

        :param backend: an object, fulfilling at least the interface
                        of :py:class:`~.backends.PyVaultBackend`. Use
                        one of the provided backends, if in doubt.
    """

    def __init__(self, backend):
        self._backend = backend
        self._meta = PyVaultMeta(self._backend)
        self._locked = True
        self._masterkey = None

    def exists(self):
        """
            :return: True if the secure storage exists, False otherwise
        """
        return self._backend.exists()

    def unlock(self, passphrase, cleanup=True):
        """
            Unlocks the encrypted storage, so that future calls to
            :py:meth:`~.PyVault.retrieve` and
            :py:meth:`~.PyVault.store` will successfully encrypt
            data and store it safely.

            This method will check the passphrase and derive the
            master key using PBKDF2. This method will always take the same
            time, wether the passphrase was correct or not.

            If the encrypted storage could not be unlocked, it will
            raise :py:class:`~.PyVaultUnlockError`.

            The speed of the unlock depends on the parameters choosen
            when creating the encrypted storage. It is deliberately "slow",
            so that brute-forcing the passphrase is not an option.

            Note, that this method will store the master key (derived
            key from your password) in memory. So as long as you do not
            lock the storage again, an attacker may potentially learn
            your master key.

            :param passphrase: Your passphrase to unlock the encrypted storage.
                               Has to be the same, you used, when creating
                               the storage.
            :param cleanup: This will cleanup the memory hold by
                            passphrase. This will ensure, that only
                            the master-key stays in memory and not
                            the passphrase used to generate it.

            :raises: :py:class:`~.PyVaultUnlockError`
        """
        self._locked = not self._meta.verify(passphrase)

        # derive masterkey from passphrase and salt
        # of vault (256bit key)
        self._masterkey = PyVaultString(
            PBKDF2(
                passphrase, self._meta.salt,
                iterations=self._meta.iterations
            ).read(64)
        )

        if cleanup:
            SecureString.clearmem(passphrase)

        if self.is_locked():
            raise PyVaultUnlockError()


    def lock(self):
        """
            This will lock the encrypted storage after it has been locked.
            This will also free up the memory region hold by the master
            key.
        """
        self._locked = True
        if not self._masterkey is None:
            self._masterkey.clear()
            self._masterkey = None

    def is_locked(self):
        """
            :return: True, if the encrypted storage is locked, and data
                     can't be read or written to it. False, otherwise.
        """
        return self._locked

    def retrieve(self, id):
        """
            :param id: a unique id that was used to store the payload

            :return: a :py:class:`PyVaultString` object, holding the
                     the decrypted payload as :py:class:`basestring`.
                     Free memory space after using the payload.

            :raises: :py:class:`ValueError`
        """
        storage = PyVaultStore(self._backend, id)
        return storage.retrieve(str(self._masterkey))

    def store(self, id, payload, cipher="aes", length=None):
        """
            :param id: a unique id to store this payload under.
            :param payload: the payload you want to store under ``id``. Has to
                            be a :py:class:`basestring` or can be converted to
                            one, when using ``str()``.
            :param cipher: select a cipher to encrypt the payload with

            .. versionadded:: 0.2.1

            :param length: length of the payload or None. If None is specified
                           then the length will be computed using
                           :py:func:`len()`.
        """
        storage = PyVaultStore(self._backend, id)
        storage.store(str(self._masterkey), payload, cipher, length)

    def create(self, passphrase, complexity=12, iterations=5000):
        """
            This will create and initialize the encrypted storage. You can
            only create the same storage once. If you loose your passphrase, the
            data stored so far, can not be recovered and is therefore lost.

            :param passhprase: the master passphrase
            :param complexity: complexity of the :py:class:`bcrypt` hashed
                               stored in the storage meta. increase this number
                               to "slow" down the unlocking process to
                               discourage brute-force attempt.
            :param iterations: number of iterations when using
                               :py:class:`PBKDF2` for deriving the master key
                               from the passphrase. increase this number to
                               "slow" down the unlocking process to
                               discourage brute-force attempts.

            :raises: :py:class:`~.pyvault.meta.PyVaultMetaInitError`
        """
        self._meta.create(passphrase, complexity, iterations)
