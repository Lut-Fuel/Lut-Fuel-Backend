from fastapi import FastAPI
from sqlmodel import SQLModel
import firebase_admin
from firebase_admin import credentials

from core.db import db_engine
from feat.home.router import home_router
from feat.trip.router import trip_router
from feat.cars.router import cars_router
from feat.dummy.router import dummy_router

# SQLModel setup
SQLModel.metadata.create_all(db_engine)


# Firebase setup
firebase_cred = credentials.Certificate(
    "core/keys/lut-fuel-firebase-adminsdk-aftnm-274f94905c.json"
)
firebase_admin.initialize_app(firebase_cred)


# FastAPI setup
app = FastAPI()

app.include_router(home_router)
app.include_router(trip_router)
app.include_router(cars_router)
app.include_router(dummy_router)
