#-*- coding: utf-8 -*-

import SecureString

class PyVaultString(object):
    def __init__(self, string):
        self._s = string

    def clear(self):
        SecureString.clearmem(self._s)

    def __repr__(self):
        return self._s

    def __str__(self):
        return self._s
