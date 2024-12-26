from textwrap import dedent
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base

from views.core import show_main_menu, show_quit_message
from views.transaction import handle_transaction_input
from views.interest_rule import handle_interest_input
from views.statement import handle_statement_input

def main():
    parser = argparse.ArgumentParser(description="Process environment settings.")
    parser.add_argument('--env', choices=['test', 'prod'], required=False, default='prod',
                        help='Specify the environment: test or prod.')

    # Parse the command-line arguments
    args = parser.parse_args()

    engine = create_engine(f"sqlite:///bank{'-test' if args.env == 'test' else ''}.db")

    Base.metadata.create_all(engine)

    SessionMaker = sessionmaker(bind=engine)
    db = SessionMaker()

    n_interactions = 0

    while True:
        '''
        Main menu
        '''
        show_main_menu(n_interactions)
        selection = input("> ").strip().upper()

        if selection == "T":
            '''
            Transactions
            '''
            handle_transaction_input(db)
            n_interactions += 1
        elif selection == "I":
            '''
            Interest rules
            '''
            handle_interest_input(db)
            n_interactions += 1
        elif selection == "P":
            '''
            Statements
            '''
            handle_statement_input(db)
            n_interactions += 1
        elif selection == "Q":
            '''
            Quit
            '''
            show_quit_message()
            db.close()
            break
        else:
            print("Invalid selection. Please select from the choices in the menu.")


if __name__ == "__main__":
    main()