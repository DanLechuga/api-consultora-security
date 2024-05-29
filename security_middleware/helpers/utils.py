from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"])


def hash_pass(password: str)->str:
    return pwd_context.hash(password)

def verify_pass(password : str,password_hash :str)->bool:
    return pwd_context.verify(password,password_hash,scheme="sha256_crypt")