# login.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from userData import get_user

router = APIRouter()

class User(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(user: User) -> Dict[str, str]:
    user_data = get_user(user.email)
    if user_data and user_data["password"] == user.password:
        return {"message": "Login successful!"}
    
    raise HTTPException(status_code=400, detail="Invalid credentials")
# from fastapi import FastAPI

# from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
# from login import router as login_router  
# from workers import router as workers_router  
# from signup import router as signup_router
# import os  # Import os module

# app = FastAPI()

# # CORS configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# app.include_router(login_router, prefix="/auth", tags=["auth"])
# app.include_router(workers_router, prefix="/api", tags=["workers"])
# app.include_router(signup_router, prefix="/auth", tags=["signup"])


# app.mount("/assets", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "assets")), name="assets")