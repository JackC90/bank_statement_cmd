from textwrap import dedent
from sqlalchemy.orm import Session

from utils.validations import validate_amount, validate_month
from utils.utils import format_date

from controllers.account import AccountController

def handle_statement_input(db: Session):
    print("")
    print(dedent("""
        Please enter account and month to generate the statement <Account> <Year><Month>
        (or enter blank to go back to main menu):
    """).strip())
    
    user_input = input("> ").strip()
    if not user_input:
        return

    parts = user_input.split()
    if len(parts) != 2:
        print("Invalid input format!")
        return

    account_id, date = parts

    if not validate_month(date):
        print("Invalid month format! Use YYYYMM")
        return

    bank_statement = AccountController.get_statement(db, account_id, date)

    print(f"\nAccount: {account_id}")
    print("| Date     | Txn Id      | Type | Amount | Balance |")
    for record in bank_statement:
        print(f"| {format_date(record['date'])} | {record['transaction_id']:<11} | {record['type']:<4} | {record['amount']:>6.2f} | {record['balance']:>7.2f} |")
