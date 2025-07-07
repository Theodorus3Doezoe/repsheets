# schemas.py
from pydantic import BaseModel

# Basis-attributen die gedeeld worden
class UserBase(BaseModel):
    email: str

# Attributen nodig bij het aanmaken van een gebruiker
class UserCreate(UserBase):
    name: str
    password: str

class UserLogin(UserBase):
    password: str


# Attributen die je teruggeeft via de API (zonder wachtwoord)
class User(UserBase):
    id: int
    name: str

    class Config:
        from_attributes = True # Vroeger orm_mode = True


class Url(BaseModel):
    url: str