import re;
STRONG_PASSWORD = re.compile("^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,18}$")
from pydantic import BaseModel, field_validator;
from pydantic.types import UUID;
from datetime import datetime;
class AccountBaseSchema(BaseModel):
    email: str;

class AccountDetail(AccountBaseSchema):
    id: UUID;
    created_at: datetime;
    updated_at: datetime;
    is_active: bool;

class AddAccount(AccountBaseSchema):
    password: str;

    @field_validator("password", mode = "after")
    @classmethod
    def validate_password(cls, password:str) -> str:
        if not re.match(STRONG_PASSWORD,password):
            raise ValueError("Password should contain at least 1 uppercase letter, 1 digit, 1 special character");
        return password;
class AccountLoginSchema(AccountBaseSchema):
    password: str;


class Token(BaseModel):
    token:str;
    type:str;
