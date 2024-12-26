from sqlalchemy.orm import Session
from sqlalchemy import func
from models.account import Account
from models.transaction import Transaction
from utils.utils import get_next_id
from datetime import datetime

class TransactionController:

    @staticmethod
    def get_transactions(db: Session, account_id: str):
       return db.query(Transaction).filter(Transaction.account_id == account_id).order_by(Transaction.id.asc()).all()

    @staticmethod
    def add_transaction(db: Session, account_id: str, date: str, type: str, amount: float) -> bool:
        account = db.query(Account).get(account_id)

        if not account:
            account = Account(id=account_id, balance=0.0)
            db.add(account)

        if type == 'W' and account.balance < amount:
            return None

        # Set new transaction ID
        date_object = datetime.strptime(date, "%Y%m%d")
        date_formatted = date_object.strftime("%Y-%m-%d")
        last_transaction = db.query(Transaction).filter(Transaction.account_id == account_id, func.date(Transaction.date) == date_formatted).order_by(Transaction.id.desc()).first()
        transaction_id = get_next_id(date, last_transaction.id if last_transaction else None)
        
        new_transaction = Transaction(
            id=transaction_id,
            account_id=account.id,
            date=date_object,
            amount=amount,
            type=type.upper()
        )
        db.add(new_transaction)
        
        if type == 'W':
            account.balance -= new_transaction.amount
        elif type == 'D':
            account.balance += new_transaction.amount

        db.commit()
            
        return new_transaction