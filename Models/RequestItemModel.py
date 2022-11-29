from pydantic import BaseModel, Field
from typing import Union

class Item(BaseModel):
    user: str
    password: str
    stock: int = Field(gt=0)