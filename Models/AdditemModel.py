from pydantic import BaseModel, Field
from typing import Union

class ItemAdd(BaseModel):
    user: str
    password: str
    name: str
    cat: int
    subcat: int