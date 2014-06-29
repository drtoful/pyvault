# PyVault

## Installation

To install PyVault from the sources:

    python setup.py install

## Disclaimer

The security of this library has of yet not been reviewed. If you're a cryptographic
genius, then please feel free to do so.

Strings can be copied arbitrarily by the interpreter (it's probably not arbitrary), so
cleaning up sensitive data (such as keys and unencrypted payload) is hard. This
is a general problem of high-level programming languages, as you don't have access
to the underlying memory directly.

Having said that, we tried to make sure, that no sensitive data remains in memory
after (un)encrypting operations. We however do not free unencrypted payload data
so you have to make sure yourself to clear it.

## License

PyVault is licensed under the BSD License. See LICENSE for more information.
