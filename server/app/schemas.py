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
class UserResponse(UserBase):
    id: int
    name: str

    class Config:
        from_attributes = True # Vroeger orm_mode = True


class Url(BaseModel):
    url: str

# Sheets schemas

# Voor het tonen van een sheet (tabblad)
class Sheet(BaseModel):
    id: int
    sheet_name: str
    position: int

    class Config:
        from_attributes = True

# Voor het maken van een nieuwe lijst (spreadsheet)
class ListCreate(BaseModel):
    list_name: str

# Voor het tonen van een lijst met de bijbehorende sheets
class List(ListCreate):
    id: int
    user_id: int
    sheets: list[Sheet] = [] # Toon de tabbladen die erin zitten

    class Config:
        from_attributes = True