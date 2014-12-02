import unittest

from nose.tools import raises
from nose.tools import assert_equal

from pyvault import PyVault
from pyvault.backends.file import PyVaultFileBackend
from pyvault.backends.ptree import PyVaultPairtreeBackend

class VaultRetrieve(unittest.TestCase):
    """
    testing retrieving previously stored data, also
    trying to retrieve data that is not in the vault
    """
    def setUp(self):
        backend = PyVaultFileBackend("/tmp/_pyvault_file")
        self.vault1 = PyVault(backend)
        self.vault1.unlock("passphrase", False)

        backend = PyVaultPairtreeBackend("/tmp/_pyvault_ptree")
        self.vault2 = PyVault(backend)
        self.vault2.unlock("passphrase", False)

    @raises(ValueError)
    def test_retrieve_unknown(self):
        self.vault1.retrieve("notfound")

    def test_retrieve_file(self):
        data = self.vault1.retrieve("key")
        assert_equal(str(data), "secret")

        data.clear()
        assert_equal(str(data), "\x00\x00\x00\x00\x00\x00")

    def test_retrieve_ptree(self):
        data = self.vault2.retrieve("key")
        assert_equal(str(data), "secret")

        data.clear()
        assert_equal(str(data), "\x00\x00\x00\x00\x00\x00")
