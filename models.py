import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import urllib
import json


Base = declarative_base()
class VenmoTransactions(Base):
    __table_args__ = {"schema":"CMP"}
    __tablename__ = 'venmoTransactions'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer)
    payment_id = Column(Integer)
    transaction_id = Column(Integer)
    date_completed = Column(DateTime)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)
    amount = Column(Float, nullable = False)
    status = Column(String(55))
    userid = Column(String(25))
    username = Column(String(100))
    first_name = Column(String(55))
    last_name = Column(String(100))
    display_name = Column(String(100))





