#!/usr/bin/env python3
"""
SHIRA — Criptografia Própria
- AES-256-GCM (simétrica)
- RSA-4096 (assimétrica)
- Hash SHA-512 com salt
- Geração de chave única por sessão
"""

import os
import hashlib
import hmac
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

class ShiraCrypto:
    def __init__(self):
        self.sessao = os.urandom(32)
        self.gerar_chaves()

    def cifrar_simetrico(self, dados):
        aesgcm = AESGCM(self.sessao)
        nonce = os.urandom(12)
        cifrado = aesgcm.encrypt(nonce, dados.encode(), b"")
        return base64.b64encode(nonce + cifrado).decode()

    def decifrar_simetrico(self, dados_cifrados):
        dados = base64.b64decode(dados_cifrados)
        nonce = dados[:12]
        cifrado = dados[12:]
        aesgcm = AESGCM(self.sessao)
        return aesgcm.decrypt(nonce, cifrado, b"").decode()

    def gerar_chaves(self):
        self.privada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        self.publica = self.privada.public_key()

    def cifrar_assimetrico(self, dados):
        cifrado = self.publica.encrypt(
            dados.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(cifrado).decode()

    def decifrar_assimetrico(self, dados_cifrados):
        cifrado = base64.b64decode(dados_cifrados)
        return self.privada.decrypt(
            cifrado,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()

    def hash_senha(self, senha, salt=None):
        if salt is None:
            salt = os.urandom(32)
        hash_obj = hashlib.sha512(salt + senha.encode()).hexdigest()
        hmac_obj = hmac.new(salt, senha.encode(), hashlib.sha512).hexdigest()
        return {
            "salt": base64.b64encode(salt).decode(),
            "hash": hash_obj,
            "hmac": hmac_obj
        }

    def verificar_senha(self, senha, dados_hash):
        salt = base64.b64decode(dados_hash["salt"])
        novo_hash = hashlib.sha512(salt + senha.encode()).hexdigest()
        novo_hmac = hmac.new(salt, senha.encode(), hashlib.sha512).hexdigest()
        return novo_hash == dados_hash["hash"] and novo_hmac == dados_hash["hmac"]

if __name__ == "__main__":
    c = ShiraCrypto()
    senha = "SHIRA-TWS-2026"
    hash_dados = c.hash_senha(senha)
    print("🔐 Senha hasheada:", hash_dados)
    print("✅ Verificação:", c.verificar_senha(senha, hash_dados))
