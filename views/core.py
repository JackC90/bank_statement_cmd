from textwrap import dedent


def show_main_menu(n_interactions):
    if not n_interactions:
        print("\nWelcome to AwesomeGIC Bank! What would you like to do?")
    else:
        print("\nIs there anything else you'd like to do?")
    print(dedent("""
    [T] Input transactions 
    [I] Define interest rules
    [P] Print statement
    [Q] Quit
    """).strip("\n"))

def show_quit_message():
    print("")
    print(dedent("""
        Thank you for banking with AwesomeGIC Bank.
        Have a nice day!
    """).strip("\n"))