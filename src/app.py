from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlmodel import SQLModel, Session
import firebase_admin
from firebase_admin import credentials
from pydantic import BaseModel

from core.db import db_engine
from feat.dummy.router import dummy_router
from feat.auth.router import get_user_id

from sqlmodel import Field, select
from typing import Optional


class CarOwnership(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    car_id: int = Field(foreign_key="car.id")
    custom_name: str
    fuel_grade: int


class History(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    car_id: int
    car_custom_name: Optional[str] = None
    fuel_needed: float
    distance: float
    from_location: str = Field(alias="from")
    destination: str
    tolls: bool
    fuel_cost: float
    toll_cost: float


class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    maker: str
    model: str
    number_of_cylinders: int
    engine_type: int
    engine_horse_power: float
    engine_horse_power_rpm: int
    transmission: int
    fuel_tank_capacity: int
    acceleration_0_to_100_km: float
    max_speed_km_per_hour: int
    fuel_grade: int
    year: int
    type_of_car: int
    car_name: str


# SQLModel setup
SQLModel.metadata.create_all(db_engine)


# Firebase setup
firebase_cred = credentials.Certificate(
    "core/keys/lut-fuel-firebase-adminsdk-aftnm-274f94905c.json"
)
firebase_admin.initialize_app(firebase_cred)


# FastAPI setup
app = FastAPI()

app.include_router(dummy_router)


@app.get("/home")
async def home(
    user_id: str = Depends(get_user_id),
):
    return {
        "message": "Home fetched successfully",
        "data": {
            "stats": {"distanceTraveled": 172.9, "fuelConsumed": 12.3},
            "cars": [
                {
                    "customName": "Toyota Supra MK4",
                    "fuelType": "Pertalite",
                },
            ],
            "history": [
                {
                    "id": 1,
                    "carName": "Toyota Supra MK4",
                    "from": "Jakarta",
                    "destination": "Bandung",
                    "fuelNeeded": 12.3,
                    "cost": 123000,
                }
            ],
        },
    }


@app.get("/history")
async def history(
    user_id: str = Depends(get_user_id),
    page: int = 0,
    size: int = 20,
):
    return {
        "message": "History fetched successfully",
        "data": [
            {
                "id": 1,
                "carName": "Toyota Supra MK4",
                "from": "Jakarta",
                "destination": "Bandung",
                "fuelNeeded": 12.3,
                "cost": 123000,
            }
        ],
    }


@app.get("/history/{id}")
async def history_detail(
    id: int,
    user_id: str = Depends(get_user_id),
):
    return {
        "message": "Cost calculated successfully",
        "data": {
            "id": 1,
            "carName": "Toyota Supra MK4",
            "carCustomName": "Supra Bapak",
            "fuelType": "Pertalite",
            "cyliner": "6 Cylinder",
            "engineVolume": "3000 cc",
            "power": "320 hp",
            "weight": "1500 kg",
            "fuelNeeded": 12.3,
            "distance": 172.9,
            "from": "Jakarta",
            "destination": "Bandung",
            "tolls": False,
            "fuelCost": 123000,
            "tollCost": 0,
            "totalCost": 123000,
        },
    }


@app.get("/users-car")
async def users_car(
    user_id: str = Depends(get_user_id),
    page: int = 0,
    size: int = 20,
):
    with Session(db_engine) as session:
        query = (
            select(CarOwnership)
            .where(CarOwnership.user_id.ilike(f"%{user_id}%"))
            .offset(page * size)
            .limit(size)
        )
        cars_ownership = session.exec(query).all()
        cars_ownership_data = [
            {
                "id": car.id,
                "customName": car.custom_name,
                "fuelType": car.fuel_grade,
                # "carName": car.car_name,
                # "cylinder": car.number_of_cylinders,
                # "engineVolume": car.engine_type,
                # "power": car.engine_horse_power,
                # "weight": car.engine_horse_power_rpm,
            }
            for car in cars_ownership
        ]
        query= (
            select(Car)
            .where(Car.id.in_([car.car_id for car in cars_ownership]))
        )
        cars = session.exec(query).all()
        cars_data = [
            {
                "carName": car.car_name,
                "cylinder": car.number_of_cylinders,
                "engineVolume": car.engine_type,
                "power": car.engine_horse_power,
                "weight": car.engine_horse_power_rpm,
            }
            for car in cars
        ]
        for i in range(len(cars_ownership_data)):
            cars_ownership_data[i].update(cars_data[i])
    return {
        "message": "User's car list fetched successfully",
        "data": cars_ownership_data,
    }


@app.get("/cars/search")
async def search_car(
    user_id: str = Depends(get_user_id),
    page: int = 0,
    size: int = 20,
    q: str = "",
):
    with Session(db_engine) as session:
        query = (
            select(Car)
            .where(Car.car_name.ilike(f"%{q}%"))
            .offset(page * size)
            .limit(size)
        )
        cars = session.exec(query).all()
        car_data = [
            {
                "id": car.id,
                "carName": car.car_name,
            }
            for car in cars
        ]

    return {
        "message": "Car list fetched successfully",
        "data": car_data,
    }


class AddUserCarRequest(BaseModel):
    customName: str
    carId: int
    fuelId: int


@app.post("/users-car")
async def add_user_car(
    request: AddUserCarRequest,
    user_id: str = Depends(get_user_id),
):
    car_ownership = CarOwnership(
        user_id=user_id, 
        car_id=request.carId,
        custom_name=request.customName, 
        fuel_grade=request.fuelId
        )
 
    with Session(db_engine) as session:
        session.add(car_ownership)
        session.commit()
    return {"message": "User's car added successfully"}


## Search Location

# - Route : `/location/search`
# - Method : `GET`
# - Header : `Authorization` : `Bearer <token>`
# - Query Parameters
#   - `q`: `string`, optional, default `""`
# - Expected Response

# ```json
# {
#   "message": "Location list fetched successfully",
#   "data": [
#     // Max 5
#     {
#       "name": "Fakultas Teknik Univ ABC",
#       "address": "Jl. ABC No. 123, Jakarta Selatan, DKI Jakarta",
#       "latitude": -6.123456,
#       "longitude": 106.123456
#     }
#   ]
# }
# ```


@app.get("/location/search")
async def search_location(
    q: str,
    user_id: str = Depends(get_user_id),
):
    return {
        "message": "Location list fetched successfully",
        "data": [
            {
                "name": "Fakultas Teknik Univ ABC",
                "address": "Jl. ABC No. 123, Jakarta Selatan, DKI Jakarta",
                "latitude": -6.123456,
                "longitude": 106.123456,
            }
        ],
    }


## Get Routes

# - Route : `/routes`
# - Method : `GET`
# - Header : `Authorization` : `Bearer <token>`
# - Query Parameters
#   - `fromLatitude`: `double`, required
#   - `fromLongitude`: `double`, required
#   - `destinationLatitude`: `double`, required
#   - `destinationLongitude`: `double`, required
# - Expected Response

# ```json
# {
#   "message": "Routes fetched successfully",
#   "data": [
#     {
#       "id": 1,
#       "name": "Route 1",
#       "tolls": false,
#       "distance": 172.9, // km
#       "duration": 230, // minutes
#       "cost": 123000, // rupiah
#       "polyline": [
#         "vs{d@yx}jSe@DYBu@H_@D]Hc@NG@c@PYLQFu@POB[J_@J_@HOBOBy@N_@F}@LcALe@HIBC?aAPQBm@JqATeAP",
#         "zrzd@oo}jSABABA?EBKB]HiC`@",
#         "zlzd@sm}jSC@SBiATkAT",
#         "lgzd@al}jSQLMFMLSRSbC"
#       ]
#     }
#   ]
# }
# ```


@app.get("/routes")
async def get_routes(
    user_id: str = Depends(get_user_id),
    fromLatitude: float = 0,
    fromLongitude: float = 0,
    destinationLatitude: float = 0,
    destinationLongitude: float = 0,
):
    return {
        "message": "Routes fetched successfully",
        "data": [
            {
                "id": 0,
                "name": "Tolls",
                "distance": 172.9,
                "duration": 230,
                "cost": 123000,
                "polyline": [
                    "vs{d@yx}jSe@DYBu@H_@D]Hc@NG@c@PYLQFu@POB[J_@J_@HOBOBy@N_@F}@LcALe@HIBC?aAPQBm@JqATeAP",
                    "zrzd@oo}jSABABA?EBKB]HiC`@",
                    "zlzd@sm}jSC@SBiATkAT",
                    "lgzd@al}jSQLMFMLSRSbC",
                ],
            },
            {
                "id": 1,
                "name": "No Tolls",
                "distance": 172.9,
                "duration": 230,
                "cost": 123000,
                "polyline": [
                    "vs{d@yx}jSe@DYBu@H_@D]Hc@NG@c@PYLQFu@POB[J_@J_@HOBOBy@N_@F}@LcALe@HIBC?aAPQBm@JqATeAP",
                    "zrzd@oo}jSABABA?EBKB]HiC`@",
                    "zlzd@sm}jSC@SBiATkAT",
                    "lgzd@al}jSQLMFMLSRSbC",
                ],
            },
        ],
    }


## Calculate Cost

# - Route : `/calculate-cost`
# - Method : `POST`
# - Header : `Authorization` : `Bearer <token>`
# - Request Body

# ```json
# {
#   "fromLatitude": -6.123456,
#   "fromLongitude": 106.123456,
#   "destinationLatitude": -6.123456,
#   "destinationLongitude": 106.123456,
#   "distance": 172.9, // km
#   "tolls": false,
#   // either userCarId or newCar is required
#   "userCarId": 1,
#   "newCar": {
#     "customName": "Supra Bapak", // optional, default car name
#     "carId": 1,
#     "fuelId": 1,
#     "saveCar": true // optional, default false
#   }
# }
# ```

# - Expected Response

# ```json
# {
#   "message": "Cost calculated successfully",
#   "data": {
#     "id": 1,
#     "carName": "Toyota Supra MK4",
#     "carCustomName": "Supra Bapak",
#     "fuelType": "Pertalite",
#     "cyliner": "6 Cylinder",
#     "engineVolume": "3000 cc",
#     "power": "320 hp",
#     "weight": "1500 kg",
#     "fuelNeeded": 12.3, // liter
#     "distance": 172.9, // km
#     "from": "Jakarta",
#     "destination": "Bandung",
#     "tolls": False,
#     "fuelCost": 123000,
#     "tollCost": 0,
#     "totalCost": 123000
#   }
# }
# ```


class NewCarRequest(BaseModel):
    customName: str
    carId: int
    fuelId: int
    saveCar: bool = False


class CalculateCostRequest(BaseModel):
    fromLatitude: float
    fromLongitude: float
    destinationLatitude: float
    destinationLongitude: float
    distance: float
    tolls: bool
    userCarId: int | None = None
    newCar: NewCarRequest | None = None


@dummy_router.post("/calculate-cost")
async def calculate_cost(
    request: CalculateCostRequest,
    user_id: str = Depends(get_user_id),
):
    return {
        "message": "Cost calculated successfully",
        "data": {
            "id": 1,
            "carName": "Toyota Supra MK4",
            "carCustomName": "Supra Bapak",
            "fuelType": "Pertalite",
            "cyliner": "6 Cylinder",
            "engineVolume": "3000 cc",
            "power": "320 hp",
            "weight": "1500 kg",
            "fuelNeeded": 12.3,  # liter
            "distance": 172.9,  # km
            "from": "Jakarta",
            "destination": "Bandung",
            "tolls": False,
            "fuelCost": 123000,
            "tollCost": 0,
            "totalCost": 123000,
        },
    }
