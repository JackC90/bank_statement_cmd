from textwrap import dedent
from sqlalchemy.orm import Session

from utils.validations import validate_amount, validate_date
from utils.utils import format_date

from controllers import TransactionController

def handle_transaction_input(db: Session):
    print("")
    print(dedent("""
        Please enter transaction details in <Date> <Account> <Type> <Amount> format
        (or enter blank to go back to main menu):
    """).strip())
    
    user_input = input("> ").strip()
    if not user_input:
        return

    parts = user_input.split()
    if len(parts) != 4:
        print("Invalid input format!")
        return

    date, account_id, type, amount = parts

    if not validate_date(date):
        print("Invalid date format! Use YYYYMMdd")
        return

    if not type.upper() in ['D', 'W']:
        print("Invalid transaction type! Use D for deposit or W for withdrawal")
        return

    if not validate_amount(amount):
        print("Invalid amount! Must be greater than zero with up to 2 decimal places")
        return

    if TransactionController.add_transaction(db, account_id, date, type, float(amount)):
        print(f"\nAccount: {account_id}")
        print("| Date     | Txn Id      | Type | Amount |")
        for transaction in TransactionController.get_transactions(db, account_id):
            print(f"| {format_date(transaction.date)} | {transaction.id:<10} | {transaction.type:<4} | {transaction.amount:>6.2f} |")
    else:
        print("Transaction failed! Insufficient funds")