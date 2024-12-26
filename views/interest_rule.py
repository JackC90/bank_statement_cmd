from textwrap import dedent
from sqlalchemy.orm import Session

from utils.validations import validate_rate, validate_date
from utils.utils import format_date

from controllers import InterestRuleController

def handle_interest_input(db: Session):
    print("")
    print(dedent("""
        Please enter interest rules details in <Date> <RuleId> <Rate in %> format
        (or enter blank to go back to main menu):
    """).strip())
    
    user_input = input("> ").strip()
    if not user_input:
        return

    parts = user_input.split()
    if len(parts) != 3:
        print("Invalid input format!")
        return

    date, rule_id, rate = parts

    if not validate_date(date):
        print("Invalid date format! Use YYYYMMdd")
        return

    if not validate_rate(rate):
        print("Invalid amount! Must be greater than zero and less than 100")
        return

    if InterestRuleController.add_interest_rule(db, rule_id, date, float(rate)):
        print(f"\nInterest rules:")
        print("| Date     | RuleId | Rate (%) |")
        for rule in InterestRuleController.get_interest_rules(db):
            print(f"| {format_date(rule.date)} | {rule.id:<6} | {rule.rate:>8.2f} |")
    else:
        print("Interest rule creation failed! Duplicate ID or invalid data.")