from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Admin, Student
from backend. auth import hash_password, verify_password, create_token

app = FastAPI(title="Smart Attendance AI")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Smart Attendance Backend Running"}


# ADMIN REGISTER
@app.post("/admin/register")
def register_admin(username: str, password: str, email: str, db: Session = Depends(get_db)):

    hashed = hash_password(password)

    admin = Admin(username=username, password=hashed, email=email)

    db.add(admin)
    db.commit()

    return {"message": "Admin created"}


# ADMIN LOGIN
@app.post("/admin/login")
def login(username: str, password: str, db: Session = Depends(get_db)):

    admin = db.query(Admin).filter(Admin.username == username).first()

    if not admin:
        return {"error": "User not found"}

    if not verify_password(password, admin.password):
        return {"error": "Wrong password"}

    token = create_token(username)

    return {"token": token}


# ADD STUDENT
@app.post("/students/add")
def add_student(
        name: str,
        usn: str,
        department: str,
        email: str,
        username: str,
        password: str,
        db: Session = Depends(get_db)
):

    hashed = hash_password(password)

    student = Student(
        name=name,
        usn=usn,
        department=department,
        email=email,
        username=username,
        password=hashed
    )

    db.add(student)
    db.commit()

    return {"message": "Student added successfully"}