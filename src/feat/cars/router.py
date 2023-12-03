from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from core.db import db_engine
from feat.cars.model import Car

cars_router = APIRouter(prefix="/cars", tags=["cars"])


@cars_router.get("/search")
async def get_all_cars(
    # user = Depends(),
    q: str = "",
):
    with Session(db_engine) as session:
        query = select(Car).where(Car.brand == q)
        cars = session.exec(query).all()
        return cars
