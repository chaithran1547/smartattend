from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base

DATABASE_URL = "mysql+mysqlconnector://root:Nomika%40143@localhost/smart_attendance"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)