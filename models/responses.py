from db import db
from sqlalchemy import Column, Integer, String


class ResponseModel(db.Model):
    __tablename__ = 'responses'
    
    id = Column(Integer, primary_key=True)
    message = Column(String)