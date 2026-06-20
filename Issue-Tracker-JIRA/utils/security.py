from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto"
)

# This will be used during Sign-UP
def hash_password(password: str):
    return pwd_context.hash(password)

# Below will be used during API login for Verification
def verify_password(password: str,  hash_password: str):
    return pwd_context.verify(password, hash_password)