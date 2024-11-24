from typing import Optional

from pydantic import BaseModel

class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    username: str
    company: str

    class Config:
        orm_mode = True

class UserSchemaCreate(UserSchemaBase):
    password: str

class UserSchemaUpdate(UserSchemaBase):
    username: Optional[str]
    password: Optional[str]
    company: Optional[str]

    