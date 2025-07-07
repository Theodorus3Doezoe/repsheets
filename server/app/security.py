# security.py
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

def get_password_hash(password: str) -> str:
    """Genereert een hash voor een platte tekst wachtwoord."""
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # De verify-methode controleert of het wachtwoord overeenkomt met de hash.
        # Als het niet overeenkomt, gooit het een VerifyMismatchError.
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        # De wachtwoorden komen niet overeen.
        return False