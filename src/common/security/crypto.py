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
"""

import multiprocessing
import os

from enum   import Enum
from typing import Optional

# noinspection PyPackageRequirements
import argon2
import nacl
import nacl.bindings
import nacl.exceptions

from src.common.exceptions import SecurityException
from src.common.utils      import separate_header


class CryptoLiterals(Enum):
    """Cryptographic variables.

    # TODO: Replace memory cost with 512*1024
    """
    BLAKE2_DIGEST_LENGTH   = 64
    SALT_LENGTH            = 32

    # Password login / key derivation
    ARGON2_TIME_COST      = 20
    ARGON2_MEMORY_COST    = 1000

    # Symmetric encryption
    XCHACHA20_NONCE_LENGTH = 24
    SYMMETRIC_KEY_LENGTH   = 32
    POLY1305_TAG_LENGTH    = 16


def derive_database_key(password: str, salt: Optional[bytes] = None) -> tuple:
    """Derive encryption key from password and salt."""

    if salt is None:
        salt = os.getrandom(CryptoLiterals.SALT_LENGTH.value, flags=0)

    key = argon2.low_level.hash_secret_raw(secret=password.encode(),
                                           salt=salt,
                                           time_cost=CryptoLiterals.ARGON2_TIME_COST.value,
                                           memory_cost=CryptoLiterals.ARGON2_MEMORY_COST.value,
                                           parallelism=multiprocessing.cpu_count(),
                                           hash_len=CryptoLiterals.SYMMETRIC_KEY_LENGTH.value,
                                           type=argon2.Type.ID)  # type: bytes
    return salt, key


def encrypt_and_sign(plaintext: bytes,       # Plaintext to encrypt
                     key:       bytes,       # 32-byte symmetric key
                     ad:        bytes = b''  # Associated data
                     ) -> bytes:             # Nonce + ciphertext + tag
    """Encrypt plaintext with XChaCha20-Poly1305 (IETF variant)."""
    if len(key) != CryptoLiterals.SYMMETRIC_KEY_LENGTH.value:
        raise SecurityException(f"Invalid key length ({len(key)} bytes).")

    nonce = os.getrandom(CryptoLiterals.XCHACHA20_NONCE_LENGTH.value, flags=0)

    try:
        ct_tag = nacl.bindings.crypto_aead_xchacha20poly1305_ietf_encrypt(plaintext, ad, nonce, key)  # type: bytes
    except nacl.exceptions.CryptoError as e:
        raise SecurityException(str(e))

    return nonce + ct_tag


def auth_and_decrypt(nonce_ct_tag: bytes,       # Nonce + ciphertext + tag
                     key:          bytes,       # 32-byte symmetric key
                     file_name:    str   = '',  # When provided, gracefully exits program when the tag is invalid
                     ad:           bytes = b''  # Associated data
                     ) -> bytes:                # Plaintext
    """Authenticate and decrypt XChaCha20-Poly1305 ciphertext.

    The Poly1305 tag is checked using constant time `sodium_memcmp`:
        https://download.libsodium.org/doc/helpers#constant-time-test-for-equality
    """
    if len(key) != CryptoLiterals.SYMMETRIC_KEY_LENGTH.value:
        raise SecurityException(f"Invalid key length ({len(key)} bytes).")

    nonce, ct_tag = separate_header(nonce_ct_tag, CryptoLiterals.XCHACHA20_NONCE_LENGTH.value)

    try:
        plaintext = nacl.bindings.crypto_aead_xchacha20poly1305_ietf_decrypt(ct_tag, ad, nonce, key)  # type: bytes
        return plaintext
    except nacl.exceptions.CryptoError:
        if file_name:
            raise SecurityException(f"Authentication of data in file '{file_name}' failed.")
        raise
