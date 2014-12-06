Data Formats
============

.. _meta_object: 

Meta Object Format
------------------

+------------+-------------------------------------------------------------------------------------------------+
| key        | description                                                                                     |
+============+=================================================================================================+
| version    | *integer* the version of the meta object                                                        |
+------------+-------------------------------------------------------------------------------------------------+
| passdigest | *string* bcrypt string with the hashed passphrase used to unlock this vault                     |
+------------+-------------------------------------------------------------------------------------------------+
| iterations | *integer* number of iterations used to derive master key from provided user passphrase (PBKDF2) |
+------------+-------------------------------------------------------------------------------------------------+
| salt       | *base64* salt to be used to derive masterkey from provided user passphrase (PBKDF2)             |
+------------+-------------------------------------------------------------------------------------------------+

Example:

.. code-block:: json

    {
        "passdigest":"$2a$05$YGBSeoeMOhM3wHX.pK86qu08F8.qGAn/D9iR0QatvPJVpJdWUCW.S",
        "version":1,
        "salt":"IdQdqeyHARY=",
        "iterations":1000
    }

.. _data_object:

Data Object Format
------------------

The data object format is used to store data in encrypted form to some persistent backend (e.g. database
or filesystem). The format is influenced by the `PasswordSafe`_ format V3. Instead of storing everything
into one file, a file for every entry is created.

All binary data is encoded using base64. Storing the same data in the same file, may result in a different
content, as salts and IVs are generated at random when storing data. The data is encrypted with session keys
stored encrypted in the same file.

The process of storing data is as follows:

1. randomly generate salt and IV
2. randomly generate session key
3. derive temporary key from masterkey using salt (e.g. PBKDF2)
4. encrypt session key with temporary key using IV
5. encrypt data using session key and new random IV

In addition a sha512 digest of the plaintext data is also stored the same way.

.. _PasswordSafe: http://sourceforge.net/p/passwordsafe/git-code/ci/master/tree/docs/formatV3.txt

Example:

.. code-block:: json

    {  
        "keys":[  
            {  
                "cipher":"aes",
                "salt":"JcSt+40lR6Q=",
                "id":"encryption",
                "key":"Y2v/C++XwjnzP91FNrofH1LfyURYCMAzGqunTtC+WGU=",
                "iv":"zAeMDBzKbAPpRGAG1eFHmg=="
            },
            {  
                "cipher":"aes",
                "salt":"PI/nG+++cBo=",
                "id":"digest",
                "key":"RZjGN8b27rma2jOllXuanhqpX/8fhvCgnndXynpy/8k=",
                "iv":"ALBeabdvBcBm5KmqZTlPwg=="
            }
        ],
        "version":1,
        "payload":{  
            "length":"xFLgi+CMHqNLJ4RX71LLyw==",
            "cipher":"aes",
            "data":"SsTxLAVReuack3n26CPTfQ==",
            "key":"encryption",
            "iv":"2ayvDh2aU5KthkhrPdlJjg=="
        },
        "digest":{  
            "cipher":"aes",
            "data":"RlhiMvnjaiFIvDbxQl/GKvtSrV4an0q4bGlouSIPKR6DcLrjGGXVRC1vtxRH8V9SA7UT43FBr02+1V+XmUc2j/B/ZqwuBb6gzAROIesILTAmbJawWx2P2ut5uXJRKptmALuM5XzWn/xUPxP2543f2WLOx+soS/QAJkAbpw7w1c8=",
            "key":"digest",
            "iv":"A4LVpK/Muqn7A78QAX0OcA=="
        }
    }
    
