API Reference
=============

Basics
------

.. autoclass:: pyvault.PyVaultUnlockError
    :show-inheritance:

.. autoclass:: pyvault.PyVault
    :members: unlock, lock, is_locked, retrieve, store, create


Backends
--------

All backends shall at least provide the following interface:

.. autoclass:: pyvault.backends.PyVaultBackend
    :members: create, get_meta, set_meta, retrieve, store

The following backends implement the above interface:

.. autoclass:: pyvault.backends.file.PyVaultFileBackend
    :show-inheritance:

.. autoclass:: pyvault.backends.mongo.PyVaultMongoBackend
    :show-inheritance:

.. autoclass:: pyvault.backends.ptree.PyVaultPairtreeBackend
    :show-inheritance:

Ciphers
-------

All Ciphers shall at least provide the following interface:

.. autoclass:: pyvault.ciphers.PyVaultCipher
    :members: encrypt, decrypt, derive_key

The following ciphers implement the above interface:

.. autoclass:: pyvault.ciphers.aes.PyVaultCipherAES
