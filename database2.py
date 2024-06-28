from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = "users2"
    username = Column("username", String, primary_key= True)
    password = Column("password", String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(bind = engine)

Session = sessionmaker(bind = engine)
session = Session()