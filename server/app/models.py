# models.py
from sqlalchemy import Column, Integer, String, VARCHAR, ForeignKey, NUMERIC, DATE, DATETIME
from sqlalchemy.orm import relationship
from .database import Base

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)

class User(BaseModel):
    __tablename__ = "users"

    name = Column(VARCHAR(255))
    email = Column(VARCHAR(255), unique=True, index=True)
    hashed_password = Column(VARCHAR(255))

    lists = relationship("List", back_populates="user")

class List(BaseModel):
    __tablename__ = "lists"

    user_id = Column(Integer, ForeignKey("users.id")) # Foreign Key naar de users tabel
    list_name = Column(VARCHAR(255))

    # Relatie naar User: Een List behoort tot één User
    # 'User' is de naam van de class
    # 'back_populates' linkt naar de 'lists' relatie in het User model
    user = relationship("User", back_populates="lists")