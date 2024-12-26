import decimal
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class InterestRule(Base):
    __tablename__ = 'interest_rules'

    id = Column(String, primary_key=True)
    date = Column(DateTime)
    rate = Column(Float)
    account_id = Column(String, ForeignKey("accounts.id"))

    account = relationship("Account", back_populates="interest_rules")