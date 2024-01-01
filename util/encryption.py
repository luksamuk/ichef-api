from argon2 import PasswordHasher

hasher = PasswordHasher()

def gen_password_hash(pw: str) -> str:
    return hasher.hash(pw)

def verify_password_hash(hash: str, password: str) -> bool:
    return hasher.verify(hash, password)

