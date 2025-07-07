from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import users, auth, scraping
from . import models

# Deze regel is belangrijk! Het zorgt ervoor dat SQLAlchemy alle tabellen
# die zijn gedefinieerd in onze modellen (geërfd van Base) aanmaakt in de database.
# Dit gebeurt alleen als de tabellen nog niet bestaan.
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(scraping.router)