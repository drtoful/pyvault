import unittest

from nose.tools import raises
from nose.tools import assert_false

from pyvault import PyVault, PyVaultUnlockError
from pyvault.backends.ptree import PyVaultPairtreeBackend

class VaultUnlock(unittest.TestCase):
    """
    Testing successful and unsuccesful vault unlocks
    """
    def setUp(self):
        self.backend = PyVaultPairtreeBackend("/tmp/_pyvault_ptree")
        self.vault = PyVault(self.backend)

    @raises(PyVaultUnlockError)
    def test_unlock_failure(self):
        self.vault.unlock("wrong")

    def test_unlock_success(self):
        self.vault.unlock("passphrase", False)
        assert_false(self.vault.is_locked())
