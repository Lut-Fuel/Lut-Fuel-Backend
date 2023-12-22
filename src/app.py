from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlmodel import SQLModel, Session
import firebase_admin
from firebase_admin import credentials
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import joblib

from core.db import db_engine
from feat.dummy.router import dummy_router
from feat.auth.router import get_user_id

from sqlmodel import Field, select
from typing import Optional

from get_polyline import get_routes, search_location

class PredictionResponse(BaseModel):
    prediction: float
    total_fuel: float
    cost_total: float

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
    fuel_id: int
    car_custom_name: Optional[str] = None
    fuel_needed: float
    distance: float
    # from_location: str = Field(alias="from")
    from_location: str
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


class SPBU_Data(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    gas_station: str
    fuel_type: str
    fuel_grade: int
    fuel_price: int

model = tf.keras.models.load_model('model.h5')
scaler = joblib.load('scaler.joblib')

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
    with Session(db_engine) as session:
        query = (
            select(History)
            .where(History.user_id.ilike(f"%{user_id}%"))
        )
        history_data = session.exec(query).all()
        distance_traveled = 0
        fuel_consumed = 0
        for history in history_data:
            distance_traveled += history.distance
            fuel_consumed += history.fuel_needed

        query = (
            select(CarOwnership)
            .where(CarOwnership.user_id.ilike(f"%{user_id}%"))
            .offset(0)
            .limit(4)
        )
        cars_ownership = session.exec(query).all()
        cars_ownership_data = [
            {
                "customName": car.custom_name,
                "fuelType": car.fuel_grade,
            }
            for car in cars_ownership
        ]

        query = (
            select(History)
            .where(History.user_id.ilike(f"%{user_id}%"))
            .offset(0)
            .limit(4)
        )
        history_data = []
        for history in session.exec(query).all():
            car = session.query(Car).filter(Car.id == history.car_id).first()
            history_data.append({
                "id": history.id,
                "carName": car.car_name,
                "from": history.from_location,
                "destination": history.destination,
                "fuelNeeded": history.fuel_needed,
                "cost": history.fuel_cost,
            })

    return {
        "message": "Home fetched successfully",
        "data": {
            "stats": 
                {
                "distanceTraveled": distance_traveled,
                "fuelConsumed": fuel_consumed,
                },
            "cars": cars_ownership_data,
            "history": history_data,
        },
    }


@app.get("/history")
async def history(
    user_id: str = Depends(get_user_id),
    page: int = 0,
    size: int = 20,
):
    with Session(db_engine) as session:
        query = (
            select(History)
            .where(History.user_id.ilike(f"%{user_id}%"))
            .offset(page * size)
            .limit(size)
        )
        history_data = []
        for history in session.exec(query).all():
            car = session.query(Car).filter(Car.id == history.car_id).first()
            history_data.append({
                "id": history.id,
                "carName": car.car_name,
                "from": history.from_location,
                "destination": history.destination,
                "fuelNeeded": history.fuel_needed,
                "cost": history.fuel_cost,
            })
    return {
        "message": "History fetched successfully",
        "data": history_data,
    }


@app.get("/history/{id}")
async def history_detail(
    id: int,
    user_id: str = Depends(get_user_id),
):
    with Session(db_engine) as session:
        query = select(History).where(History.id == id)
        history = session.exec(query).first()
        history_data = {
            "id": history.id,
            "carCustomName": history.car_custom_name,
            "fuelType": history.fuel_id,
            "distance": history.distance,
            "from": history.from_location,
            "destination": history.destination,
            "fuelNeeded": history.fuel_needed,
            "fuelCost": history.fuel_cost,
            "tollCost": history.toll_cost,
            "totalCost": history.fuel_cost + history.toll_cost,
        }
        query = select(Car).where(Car.id == history.car_id)
        car = session.exec(query).first()
        history_data.update({
            "carName": car.car_name,
            "cyliner": car.number_of_cylinders,
            "engineVolume": car.engine_type,
            "power": car.engine_horse_power,
            "weight": car.engine_horse_power_rpm,
        })
    return {
        "message": "Cost calculated successfully",
        "data": history_data,
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


@app.delete("/users-car/{id}")
async def delete_user_car(
    id: int,
    user_id: str = Depends(get_user_id),
):
    with Session(db_engine) as session:
        query = select(CarOwnership).where(CarOwnership.id == id)
        car_ownership = session.exec(query).first()
        session.delete(car_ownership)
        session.commit()
    return {"message": "User's car deleted successfully"}



@app.get("/location/search")
async def search_loc(
    q: str,
    user_id: str = Depends(get_user_id),
):
    return {
        "message": "Location list fetched successfully",
        "data": search_location(q)
    }




@app.get("/routes")
async def get_route(
    user_id: str = Depends(get_user_id),
    fromLatitude: float = 0,
    fromLongitude: float = 0,
    destinationLatitude: float = 0,
    destinationLongitude: float = 0,
):
    return {
        "message": "Routes fetched successfully",
        "data": get_routes(fromLatitude, fromLongitude, destinationLatitude, destinationLongitude),
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




@app.get('/car-data')
async def car_data(car_id: int):
    with Session(db_engine) as session:
        car = session.get(Car, car_id)
    return car

@app.post('/predict/', response_model=PredictionResponse)
async def predict(car_id: int, fuel_id: int, dist: float):
    with Session(db_engine) as session:
        car_input = session.get(Car, car_id)
        fuel_input = session.get(SPBU_Data, fuel_id)
    
    input_data = np.array([[
        car_input.number_of_cylinders,
        car_input.engine_type,
        car_input.engine_horse_power,
        car_input.engine_horse_power_rpm,
        car_input.transmission,
        car_input.fuel_tank_capacity,
        car_input.acceleration_0_to_100_km,
        fuel_input.fuel_grade
    ]])
    
    scaled_input = scaler.transform(input_data)
    prediction = model.predict(scaled_input)
    predicted_value = prediction[0][0]

    total_fuel = dist / predicted_value
    cost_total = total_fuel * fuel_input.fuel_price

    return {"prediction": predicted_value,
            "total fuel": total_fuel,
            "total cost": cost_total}




from typing import Optional
from pydantic import BaseModel

class CalculateCostRequest(BaseModel):
    carId: int
    fuelId: int
    carCustomname: Optional[str] = None
    distance: float
    fromLocation: str 
    destination: str
    fromLat: float
    fromLang: float
    destinationLat: float
    destinationLang: float
    tolls: bool
    tollCost: float


@app.post("/calculate-cost")
async def calculate_cost(
    request: CalculateCostRequest,
    user_id: str = Depends(get_user_id),
):
    prediction = await predict(request.carId, request.fuelId,request.distance)
    fuel_consumption = prediction['total fuel']
    fuel_cost = prediction['total cost'] 
    toll_cost = request.tollCost
    # if request.tolls:
    #     toll_cost = calculate_toll_cost(
    #         request.fromLat, request.fromLang, request.destinationLat, request.destinationLang
    #     )


    detail = History(
        car_id=request.carId,
        fuel_id=request.fuelId,
        car_custom_name=CarOwnership.custom_name,
        fuel_needed=float(fuel_consumption),
        distance=request.distance,
        from_location=request.fromLocation,
        destination=request.destination,
        tolls=request.tolls,
        fuel_cost=float(fuel_cost),
        toll_cost=request.tollCost,
        user_id=user_id
    )



    with Session(db_engine) as session:
        session.add(detail)
        # session.flush()
        # session.refresh(detail)
        session.commit()

    return {
        "message": "Cost calculated successfully",
        "data": {
            "car_id": request.carId,
            "fuel_id": request.fuelId,
            "car_custom_name": request.carCustomname,
            "distance": request.distance,
            "fuel_needed": float(fuel_consumption),
            "from_location": request.fromLocation,
            "destination": request.destination,
            "tolls": request.tolls,
            "fuel_cost": float(fuel_cost),
            "toll_cost": request.tollCost,
            "user_id": user_id
        }
        
    }



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
