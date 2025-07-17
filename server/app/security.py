# security.py
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from .database import get_db
from sqlalchemy.orm import Session
from . import config, models
from jose import JWTError, jwt

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
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodeer de JWT
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Haal de gebruiker op uit de database
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user