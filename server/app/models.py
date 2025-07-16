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

    # Relaties
    lists = relationship("List", back_populates="user")
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(BaseModel): 
    __tablename__ = "profile"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    currency = Column(VARCHAR(3))
    agent = Column(VARCHAR(255))
    
    # Relatie
    user = relationship("User", back_populates="profile")

class List(BaseModel):
    __tablename__ = "lists"

    user_id = Column(Integer, ForeignKey("users.id"))
    list_name = Column(VARCHAR(255))

    # Relaties
    user = relationship("User", back_populates="lists")
    sheets = relationship("Sheet", back_populates="parent_list")

class Sheet(BaseModel):
    __tablename__ = "list_sheets"

    list_id = Column(Integer, ForeignKey("lists.id"))
    sheet_name = Column(VARCHAR(255))
    position = Column(Integer, nullable=False)

    # Relaties
    parent_list = relationship("List", back_populates="sheets") # Gecorrigeerd
    products = relationship("Product", secondary="list_items", back_populates="sheets") 

class Item(BaseModel):
    __tablename__ = "list_items"

    sheet_id = Column(Integer, ForeignKey("list_sheets.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True) 

class Product(BaseModel):
    __tablename__ = "products"

    url = Column(VARCHAR(255))
    item_name = Column(VARCHAR(255))
    img_url = Column(VARCHAR(255))
    price_cny = Column(NUMERIC)
    scraped_at = Column(DATETIME)

    sheets = relationship("Sheet", secondary="list_items", back_populates="products")

class ExchangeRate(BaseModel):
    __tablename__ = "exchange_rates"

    date = Column(DATE)
    base_currency = Column(VARCHAR(3))
    target_currency = Column(VARCHAR(3))
    rate = Column(NUMERIC)