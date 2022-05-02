from werkzeug.security import generate_password_hash

import secrets
def generate_secret():
    return secrets.token_hex(16)


HOST = "localhost:5000"

SECRET_KEY = '' #Run generate secret and store the secret in instance/config.py

ADMIN = "admin"
ADMIN_PASSWORD = generate_password_hash("password")

MAXIMUM_SUBMISSIONS = 5