from typing import List,Optional
from pydantic import BaseModel

class Student(BaseModel):
    firstName:str
    lastName:str
    email:str
    phone:str
    

class RegisterStudentAcc(BaseModel):
    studentID:int
    password:str
    email:str
