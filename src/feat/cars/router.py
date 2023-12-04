from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from core.db import db_engine
from feat.cars.model import Car
from feat.auth.router import get_user_id

cars_router = APIRouter(prefix="/cars", tags=["cars"])


@cars_router.get("/search")
async def get_all_cars(
    user=Depends(get_user_id),
    q: str = "",
):
    with Session(db_engine) as session:
        print(q)
        query = select(Car).where(Car.brand.ilike(f"%{q}%"))
        cars = session.exec(query).all()
        return cars
