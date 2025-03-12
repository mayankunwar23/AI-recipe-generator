import os
import user_interface
from login_interface import LoginInterface

def main():
    try:
        # Show login interface
        login_ui = LoginInterface()
        logged_in = login_ui.run()

        if logged_in:
            # If login successful, proceed to the main interface
            run_user_interface()
        else:
            print("Login failed or canceled. Exiting...")

    except Exception as e:
        print(f"An error occurred: {e}")

def run_user_interface():
    try:
        # Initialize and run the main user interface
        ui = user_interface.UserInterface()
        ui.run()
    except Exception as e:
        print(f"Error launching user interface: {e}")

if __name__ == "__main__":
    main()


