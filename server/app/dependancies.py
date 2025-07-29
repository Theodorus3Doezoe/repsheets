# dependencies.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt

# Importeer direct vanuit je andere projectbestanden
from .database import SessionLocal
from . import config, models, security

def get_db():
    """
    Dependency die een database sessie levert voor een enkele request
    en deze altijd weer netjes sluit.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(security.oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency die de JWT-token valideert en de huidige gebruiker ophaalt.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user