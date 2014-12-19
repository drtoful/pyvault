import unittest
import os
import shutil
import hashlib

from nose.tools import assert_true
from nose.tools import assert_false
from nose.tools import assert_equal

from pyvault.backends.sptree import PyVaultShortenedPairtreeBackend

class VaultShortPairtree(unittest.TestCase):
    """
        Testing the shortened pairtree implementation
    """
    def setUp(self):
        self.backend = PyVaultShortenedPairtreeBackend("/tmp/_pyvault_sptree")

        self.hash = hashlib.sha512()
        self.hash.update("abc123")
        self.hash = self.hash.hexdigest()

    def test_01_store(self):
        self.backend.store(self.hash, {"key": 123})
        assert_true(os.path.isfile("/tmp/_pyvault_sptree/pairtree_root/c7/0b/5d/d9/eb/obj/c70b5dd9ebfb6f51d09d4132b7170c9d20750a7852f00680f65658f0310e810056e6763c34c9a00b0e940076f54495c169fc2302cceb312039271c43469507dc"))

    def test_02_retrieve(self):
        data = self.backend.retrieve(self.hash)
        assert_equal(data['key'], 123)

    def test_03_delete(self):
        assert_true(os.path.isfile("/tmp/_pyvault_sptree/pairtree_root/c7/0b/5d/d9/eb/obj/c70b5dd9ebfb6f51d09d4132b7170c9d20750a7852f00680f65658f0310e810056e6763c34c9a00b0e940076f54495c169fc2302cceb312039271c43469507dc"))
        self.backend.delete(self.hash)
        assert_false(os.path.isfile("/tmp/_pyvault_sptree/pairtree_root/c7/0b/5d/d9/eb/obj/c70b5dd9ebfb6f51d09d4132b7170c9d20750a7852f00680f65658f0310e810056e6763c34c9a00b0e940076f54495c169fc2302cceb312039271c43469507dc"))

