import unittest

from nose.tools import assert_equal

from pyvault.string import PyVaultString

class VaultUtils(unittest.TestCase):
    """
    testing some properties and stuff from the utilities
    that the vault uses
    """
    def test_string(self):
        mem_string = "test"
        vault_string = PyVaultString("test")
        assert_equal(mem_string, str(vault_string))

        vault_string.clear()

        assert_equal(mem_string, "\x00\x00\x00\x00")
        assert_equal(str(vault_string), "\x00\x00\x00\x00")
        assert_equal("test", "\x00\x00\x00\x00")
