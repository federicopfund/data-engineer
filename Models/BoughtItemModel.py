from pydantic import BaseModel, Field
from typing import Union

class BoughtItem(BaseModel):
    Cantidad: int = Field(gt=0)
    Sucursal: int = Field(ge=1, le=10)