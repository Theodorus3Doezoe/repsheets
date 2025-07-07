from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, security

# Maak de router (de 'afdeling') aan
router = APIRouter(
    prefix="/users",        # Alle paden hier beginnen met /users
    tags=["Users"]          # Het naambordje voor de API-documentatie
)

@router.get("/") # Wordt uiteindelijke pad: /users/
def get_all_users(db: Session = Depends(get_db)):
    # Logica om alle gebruikers op te halen...
    return db.query(models.User).all()

# -- READ (één) --
@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    # Zoek naar één specifieke gebruiker op basis van zijn primary key (ID).
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Gebruiker niet gevonden")
    return db_user

# -- DELETE --
@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Gebruiker niet gevonden")
    
    # Verwijder het object uit de sessie.
    db.delete(db_user)
    # Commit de transactie om de verwijdering definitief te maken.
    db.commit()
    return {"ok": True}

@router.post("/") # Wordt uiteindelijke pad: /users/
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Controleer of de gebruiker al bestaat.
    db_user_check = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_check:
        raise HTTPException(status_code=400, detail="E-mailadres is al in gebruik")
    
    # Hash het wachtwoord
    hashed_password = security.get_password_hash(user.password)

    # Maak een SQLAlchemy model-instantie aan met de data uit het schema.
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    # Voeg het nieuwe object toe aan de sessie (nog niet in de DB).
    db.add(db_user)
    # Commit de transactie, nu wordt het daadwerkelijk naar de DB geschreven.
    db.commit()
    # Refresh het object om de data die door de DB is gegenereerd (zoals de ID) op te halen.
    db.refresh(db_user)
    # Geef het SQLAlchemy-object terug. FastAPI en Pydantic (dankzij from_attributes)
    # zorgen voor de correcte omzetting naar JSON.
    return db_user
