import decimal
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from models.base import Base

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(String, primary_key=True)
    balance = Column(Float, default=0)

    transactions = relationship('Transaction', back_populates="account", lazy="dynamic")
    interest_rules = relationship('InterestRule', back_populates="account", lazy="dynamic")

    