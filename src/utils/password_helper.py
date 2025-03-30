# src/utils/password_helper.py
import bcrypt

def generar_hash(contrasena_plaintext):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(contrasena_plaintext.encode('utf-8'), salt)
    return hash.decode('utf-8')
