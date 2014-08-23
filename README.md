# PyVault

## Installation

To install PyVault from the sources:

    python setup.py install

## Dependencies

The following dependencies are automatically resolved by using the above command

* [pycrypto](https://github.com/dlitz/pycrypto) >= 2.6
* [SecureString](https://github.com/dnet/pysecstr) >= 0.1
* [pbkdf2](https://github.com/dlitz/python-pbkdf2) >= 1.3
* [py-bcrypt](http://www.mindrot.org/projects/py-bcrypt/) >= 0.4
* [pairtree](https://github.com/benosteen/pairtree) >= 0.5.2

You might have to install additional packages using your distributions package manager
to successfully build some of these dependencies. Debian based distribution can resolve
these dependencies by installing at least the following packages

    aptitude install build-essential python-dev libffi libffi-dev libssl-dev

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
