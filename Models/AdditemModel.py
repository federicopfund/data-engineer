from pydantic import BaseModel, Field
from typing import Union

class ItemAdd(BaseModel):
    user: str
    password: str
    name: str
    cat: int
    subcat: int
    sucursales: list[int]=Field(max_items=10,min_items=10)