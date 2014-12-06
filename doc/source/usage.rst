Usage
=====

A sample usage of PyVault can be seen as follows:

.. code-block:: python

    from pyvault import PyVault
    from pyvault.backends.file import PyVaultFileBackend

    backends = PyVaultFileBackend("/tmp/mystore")
    vault = PyVault(backend)

    if not vault.exists():
        vault.create()

    vault.unlock("secret passphrase")
    vault.store("testkey", "testvalue", cipher="aes")
    print vault.retrieve("testkey")
    vault.lock()

    # should raise ValueError
    vault.retrieve("testkey")

List of builtin ciphers:

* **aes**: :py:class:`pyvault.ciphers.aes.PyVaultCipherAES`

List of builtin backends:

* :py:class:`pyvault.backends.file.PyVaultFileBackend`
* :py:class:`pyvault.backends.mongo.PyVaultMongoBackend`
* :py:class:`pyvault.backends.ptree.PyVaultPairtreeBackend`
* :py:class:`pyvault.backends.sptree.PyVaultShortenedPairtreeBackend`

Adding a new backend
--------------------

Backends are responsible to store encrypted data and the metadata information
to some persistent storage (e.g. database or flat files). A new backend should
at least implement the interface of :py:class:`pyvault.backends.PyVaultBackend`.

A sample implementation of a in-memory backend is given as follows:

.. code-block:: python

    class MemoryBackend(object):
        def __init__(self):
            self.meta = {}
            self.data = {}

        def exists(self):
            return True

        def create(self):
            pass

        def get_meta(self):
            return self.meta

        def set_meta(self, meta):
            self.meta = meta

        def retrieve(self, key):
            if not key in self.data.keys():
                raise ValueError

            return self.data[key]

        def store(self, key, value):
            self.data[key] = value

This backend can now be used as any other predefined backend by initializing
a new :py:class:`pyvault.PyVault`:

.. code-block:: python

    backend = MemoryBackend()
    vault = PyVault(backend)

Adding a new cipher
-------------------

Ciphers encrypt and decrypt data to be stored or loaded from a
provided backend. A new cipher should at least implement the 
interface of :py:class:`pyvault.ciphers.PyVaultCipher`.

A sample implementation of a in-memory backend is given as follows:

.. code-block:: python

    class Rot13Cipher(object):
        def encrypt(self, key, iv, message):
            import codecs
            return codecs.encode(message, key)

        def decrypt(self, key, iv, message):
            return self.encrypt(key, iv, message)

        def derive_key(self, passphrase, salt):
            return "rot13"

New ciphers have to be registered at the cipher manager. The manager is responsible
to translate the id of a cipher (which is stored in the encrypted file) to the cipher
object.

You have to do this once, before you unlock a PyVault.

.. code-block:: python

    from pyvault.ciphers import cipher_manager
    cipher_manager.register("rot13", Rot13Cipher())

After that you can use your new cipher by providing the id of the cipher to the `store`
method.

.. code-block:: python

    vault = PyVault(...backend...)
    vault.store(key, value, cipher="rot13")
