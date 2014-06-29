# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='pyvault',
    version='0.1',
    packages=["pyvault", "pyvault.ciphers", "pyvault.backends"],
    install_requires=[
        'pycrypto >= 2.6',
        'SecureString >= 0.1',
        'pbkdf2 >= 1.3'
    ],

    # package metadata
    author="Tobias Heinzen",
    author_email="",
    url="",
    description="Simple to use library to securely store sensitive data.",
    license="BSD",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Topic :: Security',
    ]
)