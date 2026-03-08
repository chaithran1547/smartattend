from sqlalchemy import Column, Integer, String, Float, Date, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    password = Column(String(255))
    email = Column(String(100))


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    usn = Column(String(50))
    department = Column(String(100))
    email = Column(String(100))
    username = Column(String(50))
    password = Column(String(255))


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    date = Column(Date)
    time = Column(Time)
    status = Column(String(20))
    confidence = Column(Float)