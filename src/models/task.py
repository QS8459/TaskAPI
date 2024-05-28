from sqlalchemy import Column, Integer, String;
from src.db.engine import Base;

class Task(Base):
    __tablename__ = "task";
    id = Column(Integer, primary_key = True, index = True, autoincrement=True);
    description = Column(String,index = True);


