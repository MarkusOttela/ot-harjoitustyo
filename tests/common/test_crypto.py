#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorinator - Diet tracker
Copyright (C) 2023 Markus Ottela

This file is part of Calorinator.
Calorinator is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. Calorinator is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License
along with Calorinator. If not, see <https://www.gnu.org/licenses/>.

---

Author's note: The testing code here is modified from another personal project
https://github.com/maqp/tfc/blob/master/tests/common/test_crypto.py
"""

import unittest
from unittest      import mock
from unittest.mock import MagicMock


from src.common.exceptions import SecurityException
from src.common.crypto     import (derive_database_key, CryptoLiterals,
                                   encrypt_and_sign, auth_and_decrypt)


class TestArgon2Wrapper(unittest.TestCase):

    def setUp(self) :
        """Pre-test actions."""
        self.salt     = 6 * b'salt'
        self.password = 'password'

    @mock.patch('multiprocessing.cpu_count', return_value=1)
    def test_derive_database_key(self, _):
        """Test same password and salt produce the same value consistently during development."""
        salt, key = derive_database_key(self.password, self.salt)
        self.assertEqual(salt, self.salt)
        self.assertEqual(key.hex(), 'b402e985f14bb42fc10d1ed490f9d306'
                                    'f1dbbacd5aa244ee892d096fd7e3e325')

    @mock.patch('os.getrandom', side_effect=[32*b'a'])
    @mock.patch('multiprocessing.cpu_count', return_value=1)
    def test_derive_database_key_without_salt(self, *_):
        """Test same password and salt produce the same value consistently during development."""
        salt, key = derive_database_key(self.password)
        self.assertEqual(key.hex(), 'c4a7fce085d95fb5b3510a8f1054af32'
                                    'd2ae56d35a34ca892058284b2590c2ca')
        self.assertEqual(len(salt), CryptoLiterals.SALT_LENGTH.value)


class TestXChaCha20Poly1305(unittest.TestCase):
    """\
    Since HChaCha20 is a secure PRG, the XChaCha20 stream cipher derived
    from it is also semantically secure: Under some set of inputs
    (plaintext, associated data, key, and nonce), XChaCha20-Poly1305
    will output a ciphertext and a tag that are indistinguishable from
    the output of a truly random function. So again, the correctness of
    the implementation is best tested using test vectors.

    There are two slightly different test vectors available. Both KATs
    use the same plaintext, associated data, and key. However, both
    KATs use a different nonce, which will result in different
    ciphertext and tag.

    IETF test vectors:
        https://tools.ietf.org/html/draft-irtf-cfrg-xchacha-03#appendix-A.3

    Libsodium test vectors:
        Message: https://github.com/jedisct1/libsodium/blob/master/test/default/
                 aead_xchacha20poly1305.c#L22
        Ad:      https://github.com/jedisct1/libsodium/blob/master/test/default/
                 aead_xchacha20poly1305.c#L28
        Key:     https://github.com/jedisct1/libsodium/blob/master/test/default/
                 aead_xchacha20poly1305.c#L14
        Nonce:   https://github.com/jedisct1/libsodium/blob/master/test/default/
                 aead_xchacha20poly1305.c#L25
        CT+tag:  https://github.com/jedisct1/libsodium/blob/master/test/default/
                 aead_xchacha20poly1305.exp#L1

    To make the verification of the test vectors (listed below) easy,
    they are formatted in the most identical way as is possible.
    """

    ietf_plaintext = bytes.fromhex(
        '4c616469657320616e642047656e746c656d656e206f662074686520636c6173'
        '73206f66202739393a204966204920636f756c64206f6666657220796f75206f'
        '6e6c79206f6e652074697020666f7220746865206675747572652c2073756e73'
        '637265656e20776f756c642062652069742e')

    ietf_ad = bytes.fromhex(
        '50515253c0c1c2c3c4c5c6c7')

    ietf_key = bytes.fromhex(
        '808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f')

    ietf_nonce = bytes.fromhex(
        '404142434445464748494a4b4c4d4e4f5051525354555657')

    ietf_ciphertext = bytes.fromhex(
        'bd6d179d3e83d43b9576579493c0e939572a1700252bfaccbed2902c21396cbb'
        '731c7f1b0b4aa6440bf3a82f4eda7e39ae64c6708c54c216cb96b72e1213b452'
        '2f8c9ba40db5d945b11b69b982c1bb9e3f3fac2bc369488f76b2383565d3fff9'
        '21f9664c97637da9768812f615c68b13b52e')

    ietf_tag = bytes.fromhex(
        'c0875924c1c7987947deafd8780acf49')

    nonce_ct_tag_ietf = ietf_nonce + ietf_ciphertext + ietf_tag

    # ---

    libsodium_plaintext = \
        b"Ladies and Gentlemen of the class of '99: If I could offer you " \
        b"only one tip for the future, sunscreen would be it."

    libsodium_ad = bytes([
        0x50, 0x51, 0x52, 0x53, 0xc0, 0xc1, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7])

    libsodium_key = bytes([
        0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
        0x88, 0x89, 0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f,
        0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97,
        0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f])

    libsodium_nonce = bytes([
        0x07, 0x00, 0x00, 0x00, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47,
        0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f, 0x50, 0x51, 0x52, 0x53])

    libsodium_ct_tag = bytes([
         0xf8,0xeb,0xea,0x48,0x75,0x04,0x40,0x66
        ,0xfc,0x16,0x2a,0x06,0x04,0xe1,0x71,0xfe
        ,0xec,0xfb,0x3d,0x20,0x42,0x52,0x48,0x56
        ,0x3b,0xcf,0xd5,0xa1,0x55,0xdc,0xc4,0x7b
        ,0xbd,0xa7,0x0b,0x86,0xe5,0xab,0x9b,0x55
        ,0x00,0x2b,0xd1,0x27,0x4c,0x02,0xdb,0x35
        ,0x32,0x1a,0xcd,0x7a,0xf8,0xb2,0xe2,0xd2
        ,0x50,0x15,0xe1,0x36,0xb7,0x67,0x94,0x58
        ,0xe9,0xf4,0x32,0x43,0xbf,0x71,0x9d,0x63
        ,0x9b,0xad,0xb5,0xfe,0xac,0x03,0xf8,0x0a
        ,0x19,0xa9,0x6e,0xf1,0x0c,0xb1,0xd1,0x53
        ,0x33,0xa8,0x37,0xb9,0x09,0x46,0xba,0x38
        ,0x54,0xee,0x74,0xda,0x3f,0x25,0x85,0xef
        ,0xc7,0xe1,0xe1,0x70,0xe1,0x7e,0x15,0xe5
        ,0x63,0xe7,0x76,0x01,0xf4,0xf8,0x5c,0xaf
        ,0xa8,0xe5,0x87,0x76,0x14,0xe1,0x43,0xe6
        ,0x84,0x20])

    nonce_ct_tag_libsodium = libsodium_nonce + libsodium_ct_tag

    def setUp(self) :
        """Pre-test actions."""
        self.assertEqual(self.ietf_plaintext, self.libsodium_plaintext)
        self.assertEqual(self.ietf_ad,        self.libsodium_ad)
        self.assertEqual(self.ietf_key,       self.libsodium_key)

        self.assertNotEqual(self.ietf_nonce,        self.libsodium_nonce)
        self.assertNotEqual(self.nonce_ct_tag_ietf, self.nonce_ct_tag_libsodium)

        self.plaintext       = self.ietf_plaintext
        self.associated_data = self.ietf_ad
        self.key             = self.ietf_key

    @mock.patch('os.getrandom', side_effect=[ietf_nonce, libsodium_nonce])
    def test_encrypt_and_sign_with_the_official_test_vectors(self, mock_csprng: MagicMock) :
        self.assertEqual(encrypt_and_sign(self.plaintext,
                                          self.key,
                                          self.associated_data),
                         self.nonce_ct_tag_ietf)

        self.assertEqual(encrypt_and_sign(self.plaintext,
                                          self.key,
                                          self.associated_data),
                         self.nonce_ct_tag_libsodium)

        mock_csprng.assert_called_with(CryptoLiterals.XCHACHA20_NONCE_LENGTH.value, flags=0)

    def test_auth_and_decrypt_with_the_official_test_vectors(self) :
        self.assertEqual(auth_and_decrypt(self.nonce_ct_tag_ietf,
                                          self.key,
                                          associated_data=self.associated_data),
                         self.plaintext)
        self.assertEqual(auth_and_decrypt(self.nonce_ct_tag_libsodium,
                                          self.key,
                                          associated_data=self.associated_data),
                         self.plaintext)

    def test_invalid_size_key_raises_security_exception(self) :
        invalid_keys = [key_length * b'a' for key_length in
                        [1, CryptoLiterals.SYMMETRIC_KEY_LENGTH.value-1,
                            CryptoLiterals.SYMMETRIC_KEY_LENGTH.value+1, 1000]]
        for invalid_key in invalid_keys:
            with self.assertRaises(SecurityException):
                encrypt_and_sign(self.libsodium_plaintext, invalid_key)
            with self.assertRaises(SecurityException):
                auth_and_decrypt(self.nonce_ct_tag_ietf, invalid_key)

    @mock.patch('os.getrandom', return_value=(CryptoLiterals.XCHACHA20_NONCE_LENGTH.value-1)*b'a')
    def test_invalid_nonce_when_encrypting_raises_security_exception(self, _: MagicMock) :
        with self.assertRaises(SecurityException):
            encrypt_and_sign(self.plaintext, self.key)

    def test_invalid_tag_in_ciphertext_raises_security_exception(self) :
        with self.assertRaises(SecurityException):
            auth_and_decrypt(self.nonce_ct_tag_ietf,
                             key=bytes(CryptoLiterals.SYMMETRIC_KEY_LENGTH.value))


if __name__ == '__main__':
    unittest.main(exit=False)
