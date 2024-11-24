from typing import Optional

from pydantic import BaseModel

class AddressSchemaBase(BaseModel):

    id: Optional[int] = None
    description: str
    lat: float
    long: float

    class Config:
        orm_mode = True



