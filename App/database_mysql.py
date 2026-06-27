import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("MYSQL_DATABASE_URL", "mysql+pymysql://shule_dev:dev_shule_pass@localhost:3306/zanzibar_academy_local")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency kupata DB session kwenye routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()