import hashlib
import hmac
import os

from database import create_user, get_user

MIN_PASSWORD_LENGTH = 8


def _scrypt(password, salt):
    return hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)


def hash_password(password):
    salt = os.urandom(16)
    return salt.hex() + ":" + _scrypt(password, salt).hex()


def verify_password(password, stored):
    salt_hex, digest_hex = stored.split(":")
    candidate = _scrypt(password, bytes.fromhex(salt_hex))
    return hmac.compare_digest(candidate, bytes.fromhex(digest_hex))


def sign_up(username, password):
    username = username.strip().lower()
    if not username or len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Enter a username and a password of at least {MIN_PASSWORD_LENGTH} characters."
    if not create_user(username, hash_password(password)):
        return False, "That username is already taken."
    return True, "Account created."


def log_in(username, password):
    user = get_user(username.strip().lower())
    if user is None or not verify_password(password, user["password_hash"]):
        return None
    return user