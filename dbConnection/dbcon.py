#dbcon.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import os
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get database configuration from environment variables
db_type = os.environ.get("DB_TYPE")
db_name = os.environ.get("DB_NAME")
db_userName = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD", "")  # Provide a default value if password is not set
db_port = os.environ.get("DB_PORT", "3306")  # Provide a default port if not set
server_ip = os.environ.get("DB_IP", "127.0.0.1")  # Provide a default server IP if not set

# Construct DATABASE_URL
DATABASE_URL = f"{db_type}://{db_userName}:{db_password}@{server_ip}:{db_port}/{db_name}"




engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

