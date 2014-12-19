import os
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

    def test_delete_file(self):
        assert_true(os.path.isfile("/tmp/_pyvault_file/8335fa56d487562de248f47befc72743334051ddffcc2c09275f665454990317594745ee17c08f798cd7dce0ba8155dcda14f6398c1d1545116520a133017c09"))
        self.vault1.delete("key")
        assert_false(os.path.isfile("/tmp/_pyvault_file/8335fa56d487562de248f47befc72743334051ddffcc2c09275f665454990317594745ee17c08f798cd7dce0ba8155dcda14f6398c1d1545116520a133017c09"))

    def test_lock_ptree(self):
        assert_true(os.path.isfile("/tmp/_pyvault_ptree/pairtree_root/83/35/fa/56/d4/87/56/2d/e2/48/f4/7b/ef/c7/27/43/33/40/51/dd/ff/cc/2c/09/27/5f/66/54/54/99/03/17/59/47/45/ee/17/c0/8f/79/8c/d7/dc/e0/ba/81/55/dc/da/14/f6/39/8c/1d/15/45/11/65/20/a1/33/01/7c/09/obj/data"))
        self.vault2.delete("key")
        assert_false(os.path.isfile("/tmp/_pyvault_ptree/pairtree_root/83/35/fa/56/d4/87/56/2d/e2/48/f4/7b/ef/c7/27/43/33/40/51/dd/ff/cc/2c/09/27/5f/66/54/54/99/03/17/59/47/45/ee/17/c0/8f/79/8c/d7/dc/e0/ba/81/55/dc/da/14/f6/39/8c/1d/15/45/11/65/20/a1/33/01/7c/09/obj/data"))
