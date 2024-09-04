from turtle import title
from sqlalchemy import Column, INTEGER, Integer,String,ForeignKey, func, DateTime, Date, Time, Boolean
from models.database import Base
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__='students'
    id=Column(Integer,primary_key=True,index=True)
    firstName=Column(String, nullable=False)
    lastName=Column(String, nullable=False)
    email=Column(String, nullable=False)
    phone=Column(String, nullable=False)
    
    
    enrolledOn = Column(DateTime, default=func.now())

    # Relationship to CourseStudentList and Attendance
    course_student_lists = relationship("CourseStudentList", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    payments = relationship("Payments", back_populates="student")
    saccs = relationship("StudentAccs", back_populates="student")


class StudentAccs(Base):
    __tablename__='studentAcc'
    id=Column(Integer,primary_key=True,index=True)
    studentID=Column(Integer,ForeignKey('students.id'))
    email=Column(String, nullable=False)
    password=Column(String, nullable=True)
    isverified=Column(Boolean, nullable=True, default=False)
    createdAt=Column(DateTime, default=func.now())
    student = relationship("Student", back_populates="saccs")

class Trainer(Base):
    __tablename__='trainers'
    id=Column(Integer,primary_key=True,index=True)
    firstName=Column(String, nullable=False)
    lastName=Column(String, nullable=False)
    email=Column(String, nullable=False, unique=True)
    phone=Column(String, nullable=False, unique=True)
    joinedOn = Column(DateTime, default=func.now())

    # Relationship to Courses
    courses = relationship("Courses", back_populates="trainer")

class CourseCategory(Base):
    __tablename__='coursecategories'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String, nullable=False)
    description=Column(String, nullable=False)
    createdAt=Column(DateTime, default=func.now())
      # Relationship to Courses
    courses = relationship("Courses", back_populates="course_category")

class Courses(Base):
    __tablename__='courses'
    id=Column(Integer,primary_key=True,index=True)
    trainerID=Column(Integer,ForeignKey('trainers.id'))
    CourseCategoryID=Column(Integer,ForeignKey('coursecategories.id'))
    name=Column(String, nullable=False)
    description=Column(String, nullable=False)
    imageUrl=Column(String, nullable=True)
    cost=Column(Integer,nullable=True)
    discount=Column(Integer, nullable=True)
    startDate=Column(Date, nullable=True)
    endDate=Column(Date, nullable=True)
    startTime=Column(Time, nullable=True)
    endTime=Column(Time, nullable=True)
    studentRequirements=Column(String, nullable=True)
    duration=Column(String, nullable=True)
    courseDocumentationLink=Column(String, nullable=True)
    publishStatus=Column(Boolean, nullable=True)
    meetingLink=Column(String, nullable=True)
    createdAt=Column(DateTime, default=func.now())
        # Relationships
    trainer = relationship("Trainer", back_populates="courses")
    course_category = relationship("CourseCategory", back_populates="courses")
    course_student_lists = relationship("CourseStudentList", back_populates="course")
    attendances = relationship("Attendance", back_populates="course")
    course_structures = relationship("CourseStructure", back_populates="course")


class CourseStudentList(Base):
    __tablename__='courseStudentList'
    id=Column(Integer,primary_key=True,index=True)
    StudentID=Column(Integer,ForeignKey('students.id'))
    courseID=Column(Integer,ForeignKey('courses.id'))
    joinedAt=Column(DateTime, default=func.now())
    # Relationships
    student = relationship("Student", back_populates="course_student_lists")
    course = relationship("Courses", back_populates="course_student_lists")

class Attendance(Base):
    __tablename__='attendance'
    id=Column(Integer,primary_key=True,index=True)
    studentID=Column(Integer,ForeignKey('students.id'))
    courseID=Column(Integer,ForeignKey('courses.id'))
    date=Column(Date, nullable=False)
    attendance=Column(Boolean, nullable=False)
   # Relationships
    student = relationship("Student", back_populates="attendances")
    course = relationship("Courses", back_populates="attendances")

class Payments(Base):
    __tablename__='payments'
    id=Column(Integer,primary_key=True,index=True)
    studentID=Column(Integer,ForeignKey('students.id'))
    transCode=Column(String, nullable=False)
    amount=Column(Integer, nullable=False)
    paidAt=Column(DateTime, default=func.now())
     # Relationship to Student
    student = relationship("Student", back_populates="payments")

class CourseStructure(Base):
    __tablename__ = 'course_structure'
    id = Column(Integer, primary_key=True, index=True)
    courseID = Column(Integer, ForeignKey('courses.id'), nullable=False)
    topicName = Column(String, nullable=False)
    description = Column(String, nullable=True)
    startDate = Column(Date, nullable=True)
    endDate = Column(Date, nullable=True)

    # Relationship with the Courses model
    course = relationship("Courses", back_populates="course_structures")