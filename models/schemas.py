from typing import List,Optional
from pydantic import BaseModel
from datetime import datetime

class Student(BaseModel):
    firstName:str
    lastName:str
    email:str
    phone:str
    

class RegisterStudentAcc(BaseModel):
    studentID:int
    password:str
    email:str

class StudentAccountResponse(RegisterStudentAcc):
    id:int
    isverified:bool
    createdAt:datetime
