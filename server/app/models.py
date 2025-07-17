# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, NUMERIC, DATE, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))

    # Relaties
    lists = relationship("List", back_populates="user")
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(BaseModel): 
    __tablename__ = "profile"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    currency = Column(String(3))
    agent = Column(String(255))
    
    # Relatie
    user = relationship("User", back_populates="profile")

class List(BaseModel):
    __tablename__ = "lists"

    user_id = Column(Integer, ForeignKey("users.id"))
    list_name = Column(String(255))

    # Relaties
    user = relationship("User", back_populates="lists")
    sheets = relationship("Sheet", back_populates="parent_list")

class Sheet(BaseModel):
    __tablename__ = "list_sheets"

    list_id = Column(Integer, ForeignKey("lists.id"))
    sheet_name = Column(String(255))
    position = Column(Integer, nullable=False)

    # Relaties
    parent_list = relationship("List", back_populates="sheets") # Gecorrigeerd
    products = relationship("Product", secondary="list_items", back_populates="sheets") 

class Item(BaseModel):
    __tablename__ = "list_items"

    sheet_id = Column(Integer, ForeignKey("list_sheets.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True) 
    item_name = Column(String(255))

class Product(BaseModel):
    __tablename__ = "products"

    url = Column(String(255), unique=True, index=True)
    img_url = Column(String(255))
    price_cny = Column(NUMERIC)
    scraped_at = Column(DateTime, default=datetime.now)

    sheets = relationship("Sheet", secondary="list_items", back_populates="products")

class ExchangeRate(BaseModel):
    __tablename__ = "exchange_rates"

    date = Column(DATE)
    base_currency = Column(String(3))
    target_currency = Column(String(3))
    rate = Column(NUMERIC)