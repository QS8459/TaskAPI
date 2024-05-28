from src.config import DB_URL
from sqlalchemy import create_engine, MetaData;
from sqlalchemy.orm import sessionmaker;
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base;


engine = create_engine(DB_URL, isolation_level="SERIALIZABLE");
Session = sessionmaker(bind=engine,autoflush=False);
session = Session();
inspector = inspect(engine);
metadata = MetaData();
Base = declarative_base(metadata=metadata);

def get_db():
    db = Session();
    try:
        yield db;
    finally:
        db.close();
