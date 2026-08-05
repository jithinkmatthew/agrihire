import os
from dotenv import load_dotenv

load_dotenv()

dbhost = os.getenv("DB_HOST")
dbuser = os.getenv("DB_USER")
dbpass = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
dbport = os.getenv("DB_PORT")
