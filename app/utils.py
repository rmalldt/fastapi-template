from passlib.context import CryptContext

# Cryptography context - helper function for verifying and hashing password
# In this case:
#   - schemes:    List hashing algorithms, in this case only `bcrypt`
#   - deprecated: If any added algorithm in the schemes list is deprecated, it will be marked as deprecated
pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pw(password: str) -> str:
    return pw_context.hash(password)


def verify_pw(plain_pw: str, hashed_pw: str) -> bool:
    return pw_context.verify(plain_pw, hashed_pw)
