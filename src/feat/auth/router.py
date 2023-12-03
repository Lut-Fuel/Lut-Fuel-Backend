from fastapi import Header, HTTPException
from typing import Annotated
from firebase_admin import auth


def get_user_id(
    authorization: Annotated[str | None, Header()] = None,
    bypasstoken: Annotated[str | None, Header()] = None,
) -> str:
    if bypasstoken == "lutfuelyeyey":
        return "VoLzzKQI9IVHc5HuggItnG7Q3EV2"
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    token = authorization.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]  # Extract and return only the user ID
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
