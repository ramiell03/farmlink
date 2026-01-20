import os
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
LISTING_SERVICE_URL = os.getenv("LISTING_SERVICE_URL")
DATABASE_URL= os.getenv("DATABASE_URL")