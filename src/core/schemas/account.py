from pydantic import BaseModel
from uuid import UUID
class AccountSchemaBase(BaseModel):
    email: str;


class AccountSignInSchema(AccountSchemaBase):
    password: str;
