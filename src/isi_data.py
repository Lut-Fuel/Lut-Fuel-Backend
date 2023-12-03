from feat.cars.model import Car
from core.db import db_engine
from sqlmodel import Session, select

cars = [
    Car(
        brand="Toyota",
        engine_type="V8",
        engine_hp="1000",
        weight="1000",
        cylinder="8",
    ),
    Car(
        brand="Honda",
        engine_type="V6",
        engine_hp="800",
        weight="800",
        cylinder="6",
    ),
    Car(
        brand="Suzuki",
        engine_type="V4",
        engine_hp="600",
        weight="600",
        cylinder="4",
    ),
    Car(
        brand="Yamaha",
        engine_type="V2",
        engine_hp="400",
        weight="400",
        cylinder="2",
    ),
    Car(
        brand="Ducati",
        engine_type="V1",
        engine_hp="200",
        weight="200",
        cylinder="1",
    ),
    Car(
        brand="Kawasaki",
        engine_type="V1",
        engine_hp="200",
        weight="200",
        cylinder="1",
    ),
]

with Session(db_engine) as session:
    session.add_all(cars)
    session.commit()
