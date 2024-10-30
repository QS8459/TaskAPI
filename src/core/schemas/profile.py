from pydantic import BaseModel;
from datetime import datetime;
from typing import Optional
from pydantic.types import UUID;


class ProfileBaseSchema(BaseModel):
    name: Optional[str];
    age:Optional[int];
    birth_date: Optional[datetime];
    instagram: Optional[str];
    username: Optional[str];
    facebook:Optional[str];
    about: Optional[str];
    image: Optional[str];
    
class ProfileUpdateSchema(ProfileBaseSchema):
    pass

class ProfileDetailSchema(ProfileBaseSchema):
    id: UUID;
    account: dict;