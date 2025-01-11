from pydantic import BaseModel

class TokenSchemaBase(BaseModel):
    access_tkn: str
    refresh_tkn: str