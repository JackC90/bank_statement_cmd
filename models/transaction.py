import decimal
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(String, primary_key=True)
    date = Column(DateTime)
    type = Column(String)
    amount = Column(Float)
    account_id = Column(String, ForeignKey("accounts.id"), primary_key=True)

    account = relationship("Account", back_populates="transactions")