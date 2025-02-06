"""
--
"""
import random
import string
from passlib.context import CryptContext

# import hashlib
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """---"""

    @staticmethod
    def generate_password(length=12):
        # caracteres = string.ascii_letters + string.digits + string.punctuation
        caracteres = string.digits
        password = ''.join(random.choice(caracteres) for _ in range(length))
        return password

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """---"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """---"""
        return pwd_context.hash(password)

    @staticmethod
    def generateSignature(hash):
        # Remova as quebras de linha e espaços em branco desnecessários
        private_key = Hasher.get_private_key().encode("utf-8")
        private_key = serialization.load_pem_private_key(
            private_key, password=None, backend=default_backend()
        )
        signature = private_key.sign(
            hash.encode("utf-8"), padding.PKCS1v15(), hashes.SHA1()
        )

        # return signature
        return base64.b64encode(signature).decode("utf-8")
    
    @staticmethod
    def generate_wallet_code(length=7):
        """---"""
        # caracteres = string.ascii_letters + string.digits + string.punctuation
        caracteres = string.digits
        wallet_code = "".join(random.choice(caracteres) for _ in range(length))
        return f"UNIG{wallet_code}"
