from passlib.context import CryptContext


# 비밀번호 암호화 모듈
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)      