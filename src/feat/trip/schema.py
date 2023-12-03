# contoh body
# {
#   "start": {
# 	"longitude": 2.67172,
#     "latitude": 3.45
#   },
#   "destination": {
# 	"longitude": 2.67172,
#     "latitude": 3.45
#   }
# }
from pydantic import BaseModel


class Location(BaseModel):
    longitude: float
    latitude: float


class StartTripRequest(BaseModel):
    start: Location
    destination: Location
