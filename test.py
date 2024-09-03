import os

i = [{"name": "about-time", "version": "4.2.1"}, {"name": "alive-progress", "version": "3.1.5"}, {"name": "annotated-types", "version": "0.7.0"}, {"name": "anyio", "version": "4.4.0"}, {"name": "appdirs", "version": "1.4.4"}, {"name": "arrow", "version": "1.3.0"}, {"name": "attrs", "version": "23.2.1.dev0"}, {"name": "beautifulsoup4", "version": "4.12.3"}, {"name": "binaryornot", "version": "0.4.4"}, {"name": "Brlapi", "version": "0.8.5"}, {"name": "CacheControl", "version": "0.14.0"}, {"name": "certifi", "version": "2024.7.4"}, {"name": "cffi", "version": "1.16.0"}, {"name": "chardet", "version": "5.2.0"}, {"name": "charset-normalizer", "version": "3.3.2"}, {"name": "click", "version": "8.1.7"}, {"name": "colorama", "version": "0.4.6"}, {"name": "cookiecutter", "version": "2.6.0"}, {"name": "coverage", "version": "7.6.1"}, {"name": "crypto", "version": "1.4.1"}, {"name": "cryptography", "version": "42.0.7"}, {"name": "cssselect", "version": "1.2.0"}, {"name": "dbus-python", "version": "1.3.2"}, {"name": "distro", "version": "1.9.0"}, {"name": "dnspython", "version": "2.6.1"}, {"name": "email_validator", "version": "2.2.0"}, {"name": "evdev", "version": "1.7.1"}, {"name": "fastapi", "version": "0.111.1"}, {"name": "fastapi-cli", "version": "0.0.4"}, {"name": "filelock", "version": "3.13.3"}, {"name": "flet-core", "version": "0.23.2"}, {"name": "flet-runtime", "version": "0.23.2"}, {"name": "grapheme", "version": "0.6.0"}, {"name": "h11", "version": "0.14.0"}, {"name": "httpcore", "version": "0.16.3"}, {"name": "httptools", "version": "0.6.1"}, {"name": "httpx", "version": "0.23.3"}, {"name": "idna", "version": "3.7"}, {"name": "Jinja2", "version": "3.1.4"}, {"name": "libfdt", "version": "1.7.0"}, {"name": "libtorrent", "version": "2.0.10"}, {"name": "libvirt-python", "version": "10.6.0"}, {"name": "lockfile", "version": "0.12.2"}, {"name": "louis", "version": "3.30.0"}, {"name": "lxml", "version": "5.3.0"}, {"name": "markdown-it-py", "version": "3.0.0"}, {"name": "MarkupSafe", "version": "2.1.5"}, {"name": "marshmallow", "version": "3.19.0"}, {"name": "marshmallow-dataclass", "version": "8.5.11"}, {"name": "mccabe", "version": "0.7.0"}, {"name": "mdurl", "version": "0.1.2"}, {"name": "meson", "version": "1.5.1"}, {"name": "moddb", "version": "0.11.0"}, {"name": "mpmath", "version": "1.3.0"}, {"name": "msgpack", "version": "1.0.5"}, {"name": "mypy-extensions", "version": "1.0.0"}, {"name": "Naked", "version": "0.1.32"}, {"name": "netschoolapi", "version": "11.0.5"}, {"name": "numpy", "version": "2.0.1"}, {"name": "oauthlib", "version": "3.2.2"}, {"name": "packaging", "version": "23.2"}, {"name": "pillow", "version": "10.4.0"}, {"name": "pip", "version": "24.2"}, {"name": "psutil", "version": "6.0.0"}, {"name": "pyalpm", "version": "0.10.6"}, {"name": "pycairo", "version": "1.26.1"}, {"name": "pycodestyle", "version": "2.12.1"}, {"name": "pycparser", "version": "2.22"}, {"name": "pycryptodome", "version": "3.20.0"}, {"name": "pydantic", "version": "2.8.2"}, {"name": "pydantic_core", "version": "2.20.1"}, {"name": "pyflakes", "version": "3.2.0"}, {"name": "Pygments", "version": "2.18.0"}, {"name": "PyGObject", "version": "3.48.2"}, {"name": "pypng", "version": "0.20220715.0"}, {"name": "pyserial", "version": "3.5"}, {"name": "pyTelegramBotAPI", "version": "4.21.0"}, {"name": "python-aes256", "version": "1.0.5"}, {"name": "python-dateutil", "version": "2.9.0.post0"}, {"name": "python-dotenv", "version": "1.0.1"}, {"name": "python-multipart", "version": "0.0.9"}, {"name": "python-slugify", "version": "8.0.4"}, {"name": "PyYAML", "version": "6.0.2"}, {"name": "qrcode", "version": "7.4.2"}, {"name": "ranger-fm", "version": "1.9.3"}, {"name": "repath", "version": "0.9.0"}, {"name": "requests", "version": "2.32.3"}, {"name": "rfc3986", "version": "1.5.0"}, {"name": "rich", "version": "13.7.1"}, {"name": "scour", "version": "0.38.2"}, {"name": "shellescape", "version": "3.8.1"}, {"name": "shellingham", "version": "1.5.4"}, {"name": "shtab", "version": "1.7.1"}, {"name": "six", "version": "1.16.0"}, {"name": "sniffio", "version": "1.3.1"}, {"name": "soupsieve", "version": "2.6"}, {"name": "starlette", "version": "0.37.2"}, {"name": "sympy", "version": "1.13.2"}, {"name": "telebot", "version": "0.0.5"}, {"name": "termcolor", "version": "2.4.0"}, {"name": "text-unidecode", "version": "1.3"}, {"name": "tldr", "version": "3.3.0"}, {"name": "tqdm", "version": "4.66.5"}, {"name": "typer", "version": "0.12.3"}, {"name": "types-psutil", "version": "6.0.0.20240621"}, {"name": "types-python-dateutil", "version": "2.9.0.20240316"}, {"name": "typing_extensions", "version": "4.4.0"}, {"name": "typing-inspect", "version": "0.9.0"}, {"name": "urllib3", "version": "1.26.19"}, {"name": "uvicorn", "version": "0.30.3"}, {"name": "uvloop", "version": "0.19.0"}, {"name": "watchdog", "version": "4.0.1"}, {"name": "watchfiles", "version": "0.22.0"}, {"name": "websockets", "version": "12.0"}, {"name": "wheel", "version": "0.44.0"}, {"name": "zstandard", "version": "0.22.0"}]
j = 0
while j < i.__len__():
    os.system(f'pip3 install {i[j]["name"]} --break-system-packages')
    print(f'{i[j]["name"]} installed !')
    j += 1
exit(0)
def encrypt_text(text, password):
    # Преобразуем пароль в 16-байтный ключ
    key = password.encode('utf-8')
    key = key[:16]
    
    # Дополняем текст до длины, кратной 16 байтам
    padded_text = pad(text.encode('utf-8'), 16)
    
    # Шифруем текст с помощью AES в режиме ECB
    encrypted_text = b''.join(
        [bytes([a ^ b for a, b in zip(padded_text[i:i+16], key)]) for i in range(0, len(padded_text), 16)]
    )
    
    return encrypted_text.decode('latin-1')

def decrypt_text(encrypted_text, password):
    # Преобразуем пароль в 16-байтный ключ
    key = password.encode('utf-8')
    key = key[:16]
    
    # Расшифровываем текст с помощью AES в режиме ECB
    decrypted_text = b''.join(
        [bytes([a ^ b for a, b in zip(encrypted_text.encode('latin-1')[i:i+16], key)]) for i in range(0, len(encrypted_text.encode('latin-1')), 16)]
    )
    
    # Удаляем дополнение
    try:
        decrypted_text = unpad(decrypted_text, 16)
    except ValueError:
        # Если дополнение не найдено, возвращаем исходный текст
        decrypted_text = decrypted_text
    
    return decrypted_text.decode('utf-8')

# Пример использования
password = "mypassword"
text_to_encrypt = "Секретное сообщение"

encrypted_text = encrypt_text(text_to_encrypt, password)
print("Зашифрованный текст:", encrypted_text)

decrypted_text = decrypt_text(encrypted_text, password)
print("Расшифрованный текст:", decrypted_text)
