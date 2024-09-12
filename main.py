from fastapi import Depends, FastAPI,status,Response,HTTPException
from models.database import SessionLocal, engine
import models.models as models
import models.schemas as schemas
import models.hashing as hash
from mailersend import emails
from sqlalchemy.orm import Session

app= FastAPI()
# Initialize MailerSend
mailer = emails.NewEmail('mlsn.3c84a7d321adafd58a4140910e563c259fc3cb6d84f1dd23ace599e7116f2030')
models.Base.metadata.create_all(engine)
def get_db():
    db=SessionLocal() 
    try:
        yield db
    finally:
        db.close()

@app.post("/registerStudent", status_code=status.HTTP_201_CREATED)
def registerStudent(request:schemas.Student, db:Session=Depends(get_db)):
    # hashed_password=pwd_context.hash(request.password)
    try:
        new_user=models.Student(firstName=request.firstName, lastName=request.lastName, email=request.email, phone=request.phone)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR ,detail=f"An error occurred when saving the info in the db")

    return new_user

@app.post("/createAcc", status_code=status.HTTP_201_CREATED)
def createacc(request:schemas.RegisterStudentAcc, db:Session=Depends(get_db)):
    try:
        new_acc=models.StudentAccs(studentID=request.studentID, email=request.email, password=hash.Hash.bcrypt(request.password))
        db.add(new_acc)
        db.commit()
        db.refresh(new_acc)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR ,detail=f"An error occurred when saving the info in the db")
    return {"Message":"Account Created Successfully"}

@app.get('/student-accounts', response_model=list[schemas.StudentAccountResponse])
def get_accs(db:Session=Depends(get_db)):
    accounts = db.query(models.StudentAccs).all()
    return accounts