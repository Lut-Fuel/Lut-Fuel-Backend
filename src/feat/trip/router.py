from fastapi import APIRouter, Depends, HTTPException
from feat.auth.router import get_user_id
from feat.trip.schema import StartTripRequest

trip_router = APIRouter(prefix="/trip")


@trip_router.post("/start")
async def start_trip(
    body: StartTripRequest,
    user_id: str = Depends(get_user_id),
):
    return {
        "message": "Berhasil start trip",
        "user_id": user_id,
        "body": body,
    }
