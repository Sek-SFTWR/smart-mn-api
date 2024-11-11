# signup.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from userData import add_user, get_user

router = APIRouter()

class UserSignUp(BaseModel):
    name: str
    email: str
    password: str

@router.post("/signup")
async def signup(user: UserSignUp) -> Dict[str, str]:
    if get_user(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    add_user(user.email, user.name, user.password)  # Save user data
    return {"message": "Sign up successful!"}
