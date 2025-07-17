from dotenv import load_dotenv
import os

# Laadt de variabelen uit het .env-bestand in de omgeving
load_dotenv()

# Haal de variabelen op uit de omgeving
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))