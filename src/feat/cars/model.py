from sqlmodel import Field, SQLModel
from typing import Optional


class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    brand: str
    engine_type: str
    engine_hp: str
    weight: str
    cylinder: str
