# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    # Maak een nieuwe database-sessie aan voor één enkele request.
    db = SessionLocal()
    try:
        # 'yield' geeft de sessie door aan het endpoint. De code van het endpoint
        # wordt hier uitgevoerd.
        yield db
    finally:
        # Na afloop van de request (of als er een fout optreedt), wordt de
        # sessie altijd netjes gesloten. Dit is cruciaal om database-verbindingen
        # vrij te geven.
        db.close()