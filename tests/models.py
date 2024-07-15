from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String, unique=True)
    course_id = Column(Integer)

class Courses(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key= True)
    course_name = Column(String, unique= True)
    course_fees = Column(Integer)


DATABASE_URL = "mysql+pymysql://user:password@localhost/test_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)