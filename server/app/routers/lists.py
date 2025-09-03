from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependancies import get_db, get_current_user
from ..utils import parse_product_url, scrape_product, ScrapeError


router = APIRouter(
    prefix="/lists",
    tags=["Lists & Sheets"]
)

# Endpoint om een nieuwe lijst (spreadsheet) aan te maken
@router.post("/", response_model=schemas.List, status_code=status.HTTP_201_CREATED)
def create_list(
    list_data: schemas.ListCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Maakt een nieuwe lijst aan voor de ingelogde gebruiker.
    Een standaard tabblad ('sheet1') wordt automatisch toegevoegd.
    """
    # 1. Maak de nieuwe lijst aan, gekoppeld aan de gebruiker
    new_list = models.List(
        list_name=list_data.list_name, 
        user_id=current_user.id
    )
    db.add(new_list)
    db.commit() # Commit om een ID voor new_list te krijgen
    db.refresh(new_list)

    # 2. Maak het standaard tabblad ("sheet1") aan
    default_sheet = models.Sheet(
        sheet_name="sheet1",
        list_id=new_list.id,
        position=1
    )
    db.add(default_sheet)
    db.commit()
    db.refresh(new_list) # Refresh de lijst om de nieuwe sheet relatie te laden

    return new_list

# Endpoint om alle lijsten van de ingelogde gebruiker op te halen
@router.get("/", response_model=list[schemas.List])
def get_user_lists(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Haalt alle lijsten op die eigendom zijn van de huidige gebruiker.
    """
    return db.query(models.List).filter(models.List.user_id == current_user.id).all()

# Plaats dit in je routers/lists.py bestand

@router.post("/sheets/{sheet_id}/products", status_code=status.HTTP_201_CREATED)
def add_product_to_sheet(
    sheet_id: int,
    url_data: schemas.AddItem,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 1. Controleer of de sheet bestaat en of de gebruiker de eigenaar is
    sheet = db.query(models.Sheet).filter(models.Sheet.id == sheet_id).first()
    if not sheet:
        raise HTTPException(status_code=404, detail="Sheet not found")
    
    if sheet.parent_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this sheet")

    # 2. HERGEBRUIK JE SCRAPE-LOGICA
    # Check of het product al in de database staat
    product = db.query(models.Product).filter(models.Product.url == url_data.url).first()

    if not product:
        # Product niet gevonden, dus scrapen
        converted_url = parse_product_url(url_data.url)
        try:
            image_url, cleaned_price = scrape_product(converted_url)
        except ScrapeError as e:
            raise HTTPException(status_code=400, detail=f"Kon product niet scrapen: {e}")
        
        # Maak nieuw product aan en sla op
        product = models.Product(
            url=url_data.url, 
            img_url=image_url, 
            price_cny=cleaned_price
        )
        db.add(product)
        db.commit()
        db.refresh(product)

    # 3. KOPPEL HET PRODUCT AAN DE SHEET
    # Maak een nieuwe koppeling in de 'list_items' tabel
    item = db.query(models.Item).filter(models.Item.product_id == product.id).first()

    if item:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "Product staat al in je lijst", "item_name": item.item_name}
        )

    new_item = models.Item(
        sheet_id=sheet.id,
        product_id=product.id,
        item_name=url_data.item_name
        # Je kunt hier later nog andere velden toevoegen, zoals 'item_name'
    )
    db.add(new_item)
    db.commit()

    return {"message": "Product succesvol toegevoegd aan sheet", "product_id": product.id}

# Sheet naam aanpassen

@router.patch("/sheets/{sheet_id}")
def change_sheet_name(
    sheet_id: int,
    new_name: schemas.SheetUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
     # 1. Controleer of de sheet bestaat en of de gebruiker de eigenaar is
    sheet = db.query(models.Sheet).filter(models.Sheet.id == sheet_id).first()
    if not sheet:
        raise HTTPException(status_code=404, detail="Sheet not found")
    
    if sheet.parent_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this sheet")

    sheet.sheet_name = new_name.sheet_name

    db.commit()
    db.refresh(sheet)
    
    return {"message": "Sheet naam succesvol verandert"}

#Product naam aanpassen
@router.patch("/sheets/{sheet_id}/products/{product_id}")
def change_item_name(
    sheet_id: int,
    product_id: int,
    item_data: schemas.ItemUpdate, # Gebruik je nieuwe schema
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)   
):
    item = db.query(models.Item).filter(models.Item.sheet_id == sheet_id, models.Item.product_id == product_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found in this sheet."
        )

    sheet_to_check = db.query(models.Sheet).filter(models.Sheet.id == item.sheet_id).first()
    
    # Controleer of de sheet wel bestaat en of de eigenaar klopt
    if not sheet_to_check or sheet_to_check.parent_list.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this item."
        )

    # 3. Voer de update uit
    if item_data.item_name is not None:
        item.item_name = item_data.item_name
    
    db.commit()
    db.refresh(item)
    return item

