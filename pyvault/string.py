#-*- coding: utf-8 -*-

import SecureString

class PyVaultString(object):
    def __init__(self, string):
        self._s = string

    def clear(self):
        """
        Clears memory held by the string object. Memory region will be
        filled with zeroes.

        If string was a static string, all further uses of this static
        string will be cleared as well (because the compiler correctly
        optimizes this and points to the same memory location):

        .. code-block:: python

            s = PyVaultString("test")

            print "test"
            s.clear()

            # this will print 4 zeroes
            print "test"
        """
        SecureString.clearmem(self._s)

    def __repr__(self):
        return self._s

    def __str__(self):
        return self._s
