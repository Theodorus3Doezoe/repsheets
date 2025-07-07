# models.py
from sqlalchemy import Column, Integer, String
# We importeren de 'Base' class uit ons database.py bestand.
from .database import Base

# Dit is het SQLAlchemy ORM (Object-Relational Mapping) model.
# Door te erven van Base, weet SQLAlchemy dat dit model
# gekoppeld moet worden aan een databasetabel.
class User(Base):
    # De naam van de tabel in de database.
    __tablename__ = "users"

    # De kolommen van de tabel.
    # Column definieert een kolom met een bepaald type (Integer, String, etc.).
    # primary_key=True: Dit is de unieke sleutel van de tabel.
    # index=True: Creëert een database-index op deze kolom. Dit maakt
    #             zoekopdrachten op dit veld (zoals zoeken op e-mail) veel sneller.
    # unique=True: Zorgt ervoor dat elke waarde in deze kolom uniek moet zijn.
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    # In een echte applicatie wil je hier nooit platte tekst opslaan!
    # Gebruik een bibliotheek als 'passlib' om het wachtwoord te hashen.
    hashed_password = Column(String)