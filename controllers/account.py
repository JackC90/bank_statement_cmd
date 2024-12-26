from sqlalchemy.orm import Session
from sqlalchemy import func, case
from models.account import Account
from models.transaction import Transaction
from models.interest_rule import InterestRule
from utils.utils import are_dates_same_day, is_after_day
from datetime import datetime

class AccountController:

    @staticmethod
    def get_statement(db: Session, account_id: str, date: str):
        year = int(date[:4])
        month = int(date[4:])

        start_date = datetime(year, month, 1)
        end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

        last_month_balance = db.query(func.sum(
            case(
                (Transaction.type == 'D', Transaction.amount),
                (Transaction.type == 'W', -Transaction.amount),
                else_=0
            )
        )).filter(Transaction.account_id == account_id, Transaction.date < start_date).first()
        
        month_transactions = db.query(Transaction).filter(Transaction.account_id == account_id, Transaction.date >= start_date, Transaction.date < end_date).order_by(Transaction.date.asc(), Transaction.id.asc()).all()

        first_interest_rule = db.query(InterestRule).filter(InterestRule.date < start_date).order_by(InterestRule.date.desc()).first()
        interest_rules = db.query(InterestRule).filter(InterestRule.date >= start_date, InterestRule.date < end_date).order_by(InterestRule.date.asc()).all()

        number_of_days = (end_date - start_date).days
        records = []
        current_balance = last_month_balance[0]
        current_interest_rate = first_interest_rule.rate / 100 if first_interest_rule else 0 
        transaction_index = 0
        interest_index = 0
        final_interest = 0
        current_date = start_date

        for i in range(number_of_days):
            current_date = datetime(start_date.year, start_date.month, start_date.day + i)

            # Interest rule to apply
            while interest_index < len(interest_rules):
                interest_rule = interest_rules[interest_index]

                if is_after_day(current_date, interest_rule.date):
                    break

                if are_dates_same_day(current_date, interest_rule.date):
                    current_interest_rate = interest_rule.rate / 100
                    break
                interest_index += 1

            while transaction_index < len(month_transactions):
                transaction = month_transactions[transaction_index]

                if is_after_day(current_date, transaction.date):
                    break

                if are_dates_same_day(current_date, transaction.date):
                    if transaction.type == 'W':
                        current_balance -= transaction.amount
                    elif transaction.type == 'D':
                        current_balance += transaction.amount

                    records.append({
                        "date": transaction.date,
                        "transaction_id": transaction.id,
                        "type": transaction.type,
                        "amount": transaction.amount,
                        "balance": current_balance
                    })
                transaction_index += 1
            
            # Daily interest rate
            if current_interest_rate:
                final_interest += (current_balance * current_interest_rate)

        if final_interest:
            annualized_interest = final_interest / 365
            records.append({
                 "date": current_date,
                "transaction_id": "",
                "type": "I",
                "amount": annualized_interest,
                "balance": current_balance + annualized_interest
            })

        return records












    