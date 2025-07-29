from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependancies import get_db
from .. import schemas, models, security
from jose import jwt
from .. import config
from datetime import datetime, timedelta

# Maak de router (de 'afdeling') aan
router = APIRouter(
    prefix="/auth",        # Alle paden hier beginnen met /users
    tags=["Authentication"]          # Het naambordje voor de API-documentatie
)



@router.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    #expire date
    expire = datetime.now() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(db_user.id),  # Subject: identificeert de gebruiker
        "exp": expire,         # Expiration Time: wanneer de token verloopt
    }

    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer"}