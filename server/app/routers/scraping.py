from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse, parse_qs
import re
from ..utils import parse_product_url, scrape_product, ScrapeError



router = APIRouter(
    prefix="/scrape",        # Alle paden hier beginnen met /users
    tags=["Scraping"]          # Het naambordje voor de API-documentatie
)

@router.post("/")
async def scrape(url: schemas.Url, db: Session = Depends(get_db)):
    url = url.url

    url_check = db.query(models.Product).filter(models.Product.url == url).first()
    if url_check:
        return {
            "imageUrl": url_check.img_url, 
            "price": url_check.price_cny
        }
    print("URL niet gevonden in database")

    converted_url = parse_product_url(url)
    
    try:
        image_url, cleaned_price = scrape_product(converted_url)

    except ScrapeError as e:
        raise HTTPException(status_code=400, detail=f"Kon product niet scrapen: {e}")

    
    new_product = models.Product(
    url = url, 
    img_url = image_url, 
    price_cny = cleaned_price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"imageUrl": image_url, "price": cleaned_price} 

