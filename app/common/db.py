import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://sonia:Sonia772@cluster0.nyinhhn.mongodb.net/")
DB_NAME = os.getenv("DB_NAME", "companydb")

def get_db_name():
    return DB_NAME
