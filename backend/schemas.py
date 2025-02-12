from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date  



class UserCreate(BaseModel):
    firstname: str
    lastname: str
    password: str
    email: str
    role: str = "user"  # Default role to "user"
    record_status:str

    class Config:
        from_attributes = True



class ClassCreate(BaseModel):
    class_: int  # Using class_ since `class` is a reserved keyword in Python



class SubjectCreate(BaseModel):
    subject_name: str



class TeacherCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    class_id: Optional[int] = None


class StudentCreate(BaseModel):
    firstName: str
    lastName: str
    studentID: str
    DOB: date
    classID: int
    dateOfJoin: date
    teacherID: int


class ResultCreate(BaseModel):
    studentID: int
    classID: int
    subjectID: int
    teacherID: int
    marks: float
    result_date: date

class ResultUpdate(BaseModel):
    marks: float
    result_date: date


class ResultResponse(BaseModel):
    student_id: str
    subjects_with_marks: dict
    total_marks: float

    class Config:
        from_attributes = True


class StudentLoginRequest(BaseModel):
    studentID: str
    dob: date  # Expecting a string in YYYY-MM-DD format


class TeacherAdminLoginRequest(BaseModel):
    email: str
    password: str  

