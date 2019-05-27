from models.configure import (
    Model, UNIQUE_ID, CREATED_ON, MODIFIED_ON, DELETED_ON
)
from sqlalchemy import Column, String, ForeignKey, Integer, SMALLINT, text
from flask_sqlalchemy import SQLAlchemy
__author__ = 'shashi'



class Wallet(Model):

    __tablename__ = 'wallet'
    
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)


    def to_dict(self):
        _d = dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
        return _d

class Transaction(Model):

    __tablename__ = 'transaction'
    
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    wallet_id = Column(Integer)
    type = Column(String(6))


    def to_dict(self):
        _d = dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
        return _d