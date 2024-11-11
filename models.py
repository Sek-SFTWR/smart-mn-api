from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime, timezone

class RoleEnum(str, enum.Enum):
    student = 'student'
    teacher = 'teacher'
    admin = 'admin'

# Users Table
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
 
    courses = relationship("Course", back_populates="teacher")
    enrollments = relationship("Enrollment", back_populates="student")

# Courses Table
class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    teacher_id = Column(Integer, ForeignKey('users.user_id'))
    price = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    background_image = Column(String(255))

    teacher = relationship("User", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    videos = relationship("Video", back_populates="course")
    
# Enrollments Table
class Enrollment(Base):
    __tablename__ = 'enrollments'

    enrollment_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.user_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    enrolled_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))

    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

# Videos Table
class Video(Base):
    __tablename__ = 'videos'

    video_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    vimeo_id = Column(String(50), nullable=False)
    title = Column(String(100))
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))

    course = relationship("Course", back_populates="videos")
