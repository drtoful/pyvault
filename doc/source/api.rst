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

.. autoclass:: pyvault.backends.PyVaultBackend
    :members: create, get_meta, set_meta, retrieve, store

.. autoclass:: pyvault.backends.file.PyVaultFileBackend
    :show-inheritance:

.. autoclass:: pyvault.backends.mongo.PyVaultMongoBackend
    :show-inheritance:


Ciphers
-------

You can select a specific cipher implementation by using one of the ids
below. The current list of available implementations follows.

=======   ============================================
id        implementation
=======   ============================================
aes       :py:class:`~.ciphers.aes.PyVaultCipherAES`
aescbc    see *aes*
=======   ============================================

 

.. autoclass:: pyvault.ciphers.aes.PyVaultCipherAES
