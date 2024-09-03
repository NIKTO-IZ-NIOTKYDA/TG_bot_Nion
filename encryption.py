from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from config import salt512

def encrypt(password: str, key: str) -> str:
    # Создаем ключ.
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt512,
        iterations=100000,
        backend=default_backend()
    )
    # Генерируем urlsafe base64 ключ.
    key = urlsafe_b64encode(kdf.derive(key.encode('utf-8')))

    # Создаем шифровальщик.
    cipher_suite = Fernet(key)

    # Шифруем пароль.
    encrypted_password = cipher_suite.encrypt(password.encode('utf-8'))
    
    return encrypted_password.decode('utf-8')
    

def decrypt(encrypted_password: str, key: str) -> str:

    # Создаем ключ.
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt512,
        iterations=100000,
        backend=default_backend()
    )
    # Генерируем urlsafe base64 ключ.
    key = urlsafe_b64encode(kdf.derive(key.encode('utf-8')))

    # Создаем расфровальщик.
    cipher_suite = Fernet(key)

    # Расшифруем пароль
    decrypted_password = cipher_suite.decrypt(encrypted_password.encode('utf-8'))

    return decrypted_password.decode('utf-8')
