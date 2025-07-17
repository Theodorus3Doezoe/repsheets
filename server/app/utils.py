# utils.py
import re
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def parse_product_url(url: str) -> tuple[str | None, str | None]:
    """
    Parses a product URL to extract  ID and platform.

    Returns:
        A tuple of (product_id, platform), or (None, None) if not supported.
    """
    product_id = None
    platform = None

    if "taobao.com" in url:
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            product_id = query_params.get('id', [None])[0]
            platform = "TAOBAO"
        except (IndexError, TypeError):
            pass # product_id and platform remain None

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
    
    converted_url = f"https://mulebuy.com/product?id={product_id}&platform={platform}"

    return converted_url

# Een eigen error om duidelijke fouten te geven
class ScrapeError(Exception):
    pass

def scrape_product(converted_url):
    options = Options()
    options.add_argument("--headless=new")
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(converted_url)
        wait = WebDriverWait(driver, 10)

        # Wacht op de elementen en sla ze direct op
        image_element = wait.until(
            EC.visibility_of_element_located((By.ID, "mainImage"))
        )
        price_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'CNY')]"))
        )

        # Haal de data direct uit de gevonden elementen
        image_url = image_element.get_attribute('src')
        price_text = price_element.text
        cleaned_price = price_text.replace("CNY ", "").strip()

        return image_url, cleaned_price

    except TimeoutException:
        # Gooi een duidelijke fout op als een element niet gevonden wordt
        raise ScrapeError(f"Elementen niet gevonden op {converted_url} binnen de tijdslimiet.")
    except Exception as e:
        # Vang andere onverwachte fouten op
        raise ScrapeError(f"Een onverwachte fout is opgetreden tijdens het scrapen: {e}")
    finally:
        # Sluit de browser altijd af
        driver.quit()