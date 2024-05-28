from pydantic import BaseModel;
from fastapi import FastAPI;
from src.db import Base,engine;
from src.service import router;
app = FastAPI();

Base.metadata.create_all(bind=engine)

class LoginReqBody(BaseModel):
    login: str;
    password: str;


@router.get("/")
async def read_root():
    return {"Hello": "World"}


@router.get("/users/")
async def get_uesrs():
    from src.db import Session, User;

    with Session() as s:
        users = s.query(User).all();

    return User;

app.include_router(router, prefix = "/task");