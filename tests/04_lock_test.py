import unittest

from nose.tools import assert_true
from nose.tools import assert_false

from pyvault import PyVault
from pyvault.backends.file import PyVaultFileBackend
from pyvault.backends.ptree import PyVaultPairtreeBackend

class VaultLock(unittest.TestCase):
    """
    testing locking of vault for different backends
    """
    def setUp(self):
        backend = PyVaultFileBackend("/tmp/_pyvault_file")
        self.vault1 = PyVault(backend)
        self.vault1.unlock("passphrase", False)

        backend = PyVaultPairtreeBackend("/tmp/_pyvault_ptree")
        self.vault2 = PyVault(backend)
        self.vault2.unlock("passphrase", False)

    def test_lock_file(self):
        assert_false(self.vault1.is_locked())
        self.vault1.lock()
        assert_true(self.vault1.is_locked())

    def test_lock_ptree(self):
        assert_false(self.vault2.is_locked())
        self.vault2.lock()
        assert_true(self.vault2.is_locked())
