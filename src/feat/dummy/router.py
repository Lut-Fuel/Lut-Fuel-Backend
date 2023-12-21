from fastapi import APIRouter, Depends
from feat.auth.router import get_user_id
from pydantic import BaseModel

dummy_router = APIRouter(prefix="/dummy")


@dummy_router.get("/home")
async def home(
    user_id: int = Depends(get_user_id),
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


@dummy_router.get("/history")
async def history(
    user_id: int = Depends(get_user_id),
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


@dummy_router.get("/history/{id}")
async def history_detail(
    id: int,
    user_id: int = Depends(get_user_id),
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


@dummy_router.get("/users-car")
async def users_car(
    user_id: int = Depends(get_user_id),
    page: int = 0,
    size: int = 20,
):
    return {
        "message": "User's car list fetched successfully",
        "data": [
            {
                "id": 1,
                "customName": "Supra Bapak",
                "carName": "Toyota Supra MK4",
                "fuelType": "Pertalite",
                "cylinder": "6 Cylinder",
                "engineVolume": "3000 cc",
                "power": "320 hp",
                "weight": "1500 kg",
            }
        ],
    }


@dummy_router.get("/cars/search")
async def search_car(
    user_id: int = Depends(get_user_id),
    page: int = 0,
    size: int = 20,
    q: str = "",
):
    return {
        "message": "Car list fetched successfully",
        "data": [
            {
                "id": 1,
                "carName": "Toyota Supra MK4",
            }
        ],
    }


class AddUserCarRequest(BaseModel):
    customName: str
    carId: int
    fuelId: int


@dummy_router.post("/users-car")
async def add_user_car(
    request: AddUserCarRequest,
    user_id: int = Depends(get_user_id),
):
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


@dummy_router.get("/location/search")
async def search_location(
    q: str,
    user_id: int = Depends(get_user_id),
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


@dummy_router.get("/routes")
async def get_routes(
    user_id: int = Depends(get_user_id),
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


from typing import Optional
from pydantic import BaseModel

from typing import Optional, Union
from pydantic import BaseModel

class CalculateCostRequest(BaseModel):
    fromLatitude: float
    fromLongitude: float
    destinationLatitude: float
    destinationLongitude: float
    distance: float
    tolls: bool
    userCarId: Optional[int] = None
    newCar: Optional[Union[NewCarRequest, None]] = None

class NewCarRequest(BaseModel):
    customName: str
    carId: int
    fuelId: int
    saveCar: bool = False


@dummy_router.post("/calculate-cost")
async def calculate_cost(
    request: CalculateCostRequest,
    user_id: int = Depends(get_user_id),
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
