from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, security

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

    #jwt toevoegen
    return {"status": "succes", "message": "Login succesvol"}