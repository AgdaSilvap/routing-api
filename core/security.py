from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verifiy_password(password: str, hashed: str) -> bool:
    return CRIPTO.verify(password, hashed)


def generate_password(password: str) -> str:
    return CRIPTO.hash(password)