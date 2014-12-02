import unittest
import shutil
import os
import json

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_true
from nose.tools import assert_false

from pyvault.backends.file import PyVaultFileBackend
from pyvault.backends.ptree import PyVaultPairtreeBackend
from pyvault import PyVault

class VaultCreate(unittest.TestCase):
    """
    Test if a vault can be created using different kind
    of backends.
    """
    def test_filebackend(self):
        if os.path.isdir("/tmp/_pyvault_file"):
            shutil.rmtree("/tmp/_pyvault_file")
        backend = PyVaultFileBackend("/tmp/_pyvault_file")
        vault = PyVault(backend)

        assert_true(vault.is_locked)
        vault.create("passphrase", 5, 1000)
        assert_true(vault.is_locked)
        assert_true(os.path.isdir("/tmp/_pyvault_file"))
        assert_true(os.path.isfile("/tmp/_pyvault_file/.meta"))

        with open("/tmp/_pyvault_file/.meta") as fp:
            data = json.load(fp)

        assert_equal(data['iterations'], 1000)
        assert_equal(len(data['salt']), 12)

    def test_ptreebackend(self):
        if os.path.isdir("/tmp/_pyvault_ptree"):
            shutil.rmtree("/tmp/_pyvault_ptree")
        backend = PyVaultPairtreeBackend("/tmp/_pyvault_ptree")
        vault = PyVault(backend)

        assert_true(vault.is_locked)
        vault.create("passphrase", 5, 1000)
        assert_true(vault.is_locked)
        assert_true(os.path.isdir("/tmp/_pyvault_ptree"))
        assert_true(os.path.isfile("/tmp/_pyvault_ptree/.meta"))

        with open("/tmp/_pyvault_ptree/.meta") as fp:
            data = json.load(fp)

        assert_equal(data['iterations'], 1000)
        assert_equal(len(data['salt']), 12)

