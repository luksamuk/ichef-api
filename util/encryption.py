from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

hasher = PasswordHasher()

def gen_password_hash(pw: str) -> str:
    return hasher.hash(pw)

def verify_password_hash(hash: str, password: str) -> bool:
    try:
        hasher.verify(hash, password)
        return True
    except VerifyMismatchError:
        return False
