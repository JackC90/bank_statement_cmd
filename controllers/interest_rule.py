from sqlalchemy.orm import Session
from sqlalchemy import func
from models.account import Account
from models.interest_rule import InterestRule
from utils.utils import get_next_id
from datetime import datetime

class InterestRuleController:

    @staticmethod
    def get_interest_rules(db: Session):
       return db.query(InterestRule).all()

    @staticmethod
    def add_interest_rule(db: Session, rule_id: str, date: str, rate: float) -> bool:
        # Set new interest_rule ID
        date_object = datetime.strptime(date, "%Y%m%d")
        date_formatted = date_object.strftime("%Y-%m-%d")

        if (db.query(InterestRule).get(rule_id)):
            return False

        # Remove same date rules
        db.query(InterestRule).filter(func.date(InterestRule.date) == date_formatted).delete(synchronize_session=False)

        new_interest_rule = InterestRule(
            id=rule_id,
            date=date_object,
            rate=rate
        )
        db.add(new_interest_rule)

        db.commit()
            
        return new_interest_rule