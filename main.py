from fastapi import FastAPI, HTTPException, Depends, status, Form 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated , Optional
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from enum import Enum
import auth 
from auth import get_current_user ,db_dependency
from datetime import datetime, timezone

from fastapi import UploadFile, File
import os
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(auth.router)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(get_current_user)]

# Enums for roles
class RoleEnum(str, Enum):
    student = 'student'
    teacher = 'teacher'
    admin = 'admin'

# Pydantic Models[]
class UserBase(BaseModel):
    user_id:int
    username: str
    password_hash: str
    email: str
    role: RoleEnum

class CourseBase(BaseModel):
    course_id: int
    title: str
    description: str
    teacher_id: int
    price: float
    created_at: datetime
    updated_at: datetime
    background_image: str | None = None

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class VideoBase(BaseModel):
    course_id: int
    vimeo_id: str
    title: str
    description: str

IMAGEDIR  = 'assets/images/'

# User Endpoints
@app.get('/',status_code=status.HTTP_200_OK)
async def user(user: Annotated[dict, Depends(get_current_user)], db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {'user':user}

# get post and other dynamic endpoints
@app.post("/add_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
@app.get("/users",response_model=list[UserBase],status_code=status.HTTP_200_OK)
async def read_users(db:db_dependency):
    users = db.query(models.User).all()
    return users

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Course Endpoints
# @app.post("/add_course", status_code=status.HTTP_201_CREATED)
# async def create_course(course: CourseBase, db: db_dependency):
#     db_course = models.Course(**course.model_dump())
#     db.add(db_course)
#     db.commit()
#     db.refresh(db_course)
#     return db_course

@app.post("/add_course", status_code=status.HTTP_201_CREATED)
async def create_course(
    title: str = Form(...),
    description: str = Form(...),
    teacher_id: int = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    image_path = None
    if image:
        
        os.makedirs(IMAGEDIR, exist_ok=True)
        
        
        image_path = os.path.join(IMAGEDIR, image.filename)
        
       
        contents = await image.read()
        with open(image_path, "wb") as img_file:
            img_file.write(contents)

    db_course = models.Course(
        title=title,
        description=description,
        teacher_id=teacher_id,
        price=price,
        background_image=image_path,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# this method should read all course list with teacher name
@app.get("/courses", response_model=list[CourseBase], status_code=status.HTTP_200_OK)
async def read_course(db: db_dependency):
    courses = db.query(models.Course).all()
    for course in courses:
        course.teacher_name = db.query(models.User).filter(models.User.user_id == course.teacher_id).first().username
    return courses


@app.get("/courses/{course_id}", status_code=status.HTTP_200_OK)
async def get_course(course_id: int, db: db_dependency):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

# Enrollment Endpoints
@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
async def create_enrollment(enrollment: EnrollmentBase, db: db_dependency):
    db_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@app.get("/enrollments/{enrollment_id}", status_code=status.HTTP_200_OK)
async def get_enrollment(enrollment_id: int, db: db_dependency):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.enrollment_id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return enrollment

# Video Endpoints
@app.post("/add-video", status_code=status.HTTP_201_CREATED)
async def create_video(video: VideoBase, db: db_dependency):
    db_video = models.Video(**video.model_dump())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video
@app.get("/videos",response_model=list[VideoBase], status_code=status.HTTP_200_OK)
async def read_videos(db:db_dependency):
    videos = db.query(models.Video).all()
    return videos

@app.get("/videos/{video_id}", status_code=status.HTTP_200_OK)
async def get_video(video_id: int, db: db_dependency):
    video = db.query(models.Video).filter(models.Video.video_id == video_id).first()
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    return video

@app.post("/upload-image", status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile = File(...)):

    os.makedirs(IMAGEDIR, exist_ok=True)
    file_path = os.path.join(IMAGEDIR, file.filename)
    contents = await file.read()
    with open(file_path,"wb") as buffer:
        buffer.write(contents)
    return {"filename": file.filename}
