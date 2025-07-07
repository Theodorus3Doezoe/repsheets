from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, security
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse, parse_qs
import re


router = APIRouter(
    prefix="/scrape",        # Alle paden hier beginnen met /users
    tags=["Scraping"]          # Het naambordje voor de API-documentatie
)

@router.post("/")
async def scrape(url: schemas.Url):
    #Url ophalen uit request object
    url = url.url

    #Variabelen declareren
    product_id = None
    platform = None

    #Platform en product id uit url halen.
    if "taobao.com" in url:
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            product_id = query_params.get('id', [None])[0]
            platform = "TAOBAO"
        except (IndexError, TypeError):
            pass

    elif "weidian.com" in url:
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            product_id = query_params.get('itemID', [None])[0]
            platform = "WEIDIAN"
        except (IndexError, TypeError):
            pass


    elif "1688.com" in url:
        match = re.search(r'/(\d+)\.html', url)
        if match:
            product_id = match.group(1)
            platform = "ALI_1688"

    #De url omgezet naar een mulebuy url
    converted_url = f"https://mulebuy.com/product?id={product_id}&platform={platform}"

    #Instellingen aan scraper toevoegen
    options = Options()
    options.add_argument("--headless=new")  
    prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheets": 2,

    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    #Probeer te scrapen
    try:
        #Scraper de url op
        driver.get(converted_url)
        print(f"Pagina geopend: {converted_url}")

        #Wacht tot de elementen hieronder ingeladen zijn met een limiet van 10 secondes.
        wait = WebDriverWait(driver, 10)
        
        image_element = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "product-main-image"))
        )
        price_element = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "product-price-cny"))
        )

        #Zoekt de elementen op
        try:
            image_element = driver.find_element(By.CLASS_NAME, "product-main-image")
            price_element = driver.find_element(By.CLASS_NAME, "product-price-cny")

            #Haal de data uit de elementen
            image_url = image_element.get_attribute('src')
            price_text = price_element.text
            #Verwijder de cny voor de prijs
            cleaned_price = price_text.replace("CNY ", "").strip()

        except Exception as e:
            return {"message": f"Fout: Kon een element niet vinden: {e}"}
        
    finally:
        # 4. Sluit de browser (dit gebeurt altijd, zelfs als er een fout is)
        print("\nBrowser wordt afgesloten.")
        driver.quit()
    #Stuur de gescrapte data als  een object terug
    return {"imageUrl": image_url, "price": cleaned_price} 

