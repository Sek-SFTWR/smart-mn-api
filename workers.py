from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Worker model
class Worker(BaseModel):
    name: str
    image: str
    role: str

# Sample worker data
workers_data = [
    {"name": "Sergelen", "image": "/assets/images/founder.png", "role": "Founder"},
    {"name": "D.Bilgvvn", "image": "/assets/images/ceo.png", "role": "CEO"},
    {"name": "N.Serod", "image": "/assets/images/cto.png", "role": "CTO (South Africa)"},
    {"name": "N.Serod", "image": "/assets/images/hr.png", "role": "HR Manager (India)"},
    {"name": "E.Erkhembat", "image": "/assets/images/manager.png", "role": "Project Manager"},
    {"name": "D.Bilgvvn", "image": "/assets/images/senior_backend.png", "role": "Senior Backend Developer"},
    {"name": "B.Bayarjawkhlan", "image": "/assets/images/senior-frontend.png", "role": "Senior Frontend Developer"},
    {"name": "E.Monhbat", "image": "/assets/images/sys_admin.png", "role": "System Administrator"},
]

@router.get("/workers", response_model=List[Worker])
async def read_workers():
    return workers_data
