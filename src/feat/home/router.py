from fastapi import APIRouter, Depends, HTTPException
from feat.auth.router import get_user_id

home_router = APIRouter()


@home_router.get("/")
async def home():
    return {"message": "LutFuel API is Running"}


@home_router.get("/user")
async def user(user_id: str = Depends(get_user_id)):
    return {
        "message": "Berhasil yeyey",
        "user_id": user_id,
    }
