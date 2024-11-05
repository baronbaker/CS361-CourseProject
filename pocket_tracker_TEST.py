import time
import os

class PocketTracker:
    def __init__(self):
        self.user_data = {}  # Storage for log in credentials
        self.logged_in = False
        self.current_user = None
        self.data_file = 'users.txt'
        self.load_user_data()

    def load_user_data(self): # Load user data from file
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 4:
                        username, password, spending_limit, amount_spent = parts
                        self.user_data[username] = {'password': password, 'spending_limit': float(spending_limit), 'amount_spent': float(amount_spent)}

    def save_user_data(self):   # Save user data in file
        with open(self.data_file, 'w') as file:
            for username, details in self.user_data.items():
                line = f"{username},{details['password']},{details['spending_limit']},{details['amount_spent']}\n"
                file.write(line)

    def display_welcome_message(self):
        print(" _______   _______   _______    _   __    _______   _______          _______   _______     ____     _______   _   __    _______   _______   ")
        print("|       | |       | |       |  | | / /   |       | |       |        |       | |   __  |   /    \\   |       | | | / /   |       | |   __  |  ")
        print("|    _  | |   _   | |   ____|  | |/ /    |   ____| |__   __|        |__   __| |  |__| |  /  /\\  \\  |   ____| | |/ /    |   ____| |  |__| |  ")
        print("|   |_| | |  | |  | |  |       |    \\    |  |____     | |              | |    |  _  __/ |  |__|  | |  |      |    \\    |  |____  |  _  __/  ")
        print("|    ___| |  |_|  | |  |____   |  |\\ \\   |   ____|    | |              | |    | | \\ \\   |   __   | |  |____  |  |\\ \\   |   ____| | | \\ \\    ")
        print("|   |     |       | |       |  |  | \\ \\  |  |____     | |              | |    | |  \\ \\  |  /  \\  | |       | |  | \\ \\  |  |____  | |  \\ \\   ")
        print("|___|     |_______| |_______|  |__|  \\_| |_______|    |_|              |_|    |_|   \\_\\ |__|  |__| |_______| |__|  \\_| |_______| |_|   \\_\\  \n")

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Sign Up")
            print("2. Log In")
            print("3. Exit")
            choice = input("Please select an option: ")

            if choice == "1":
                self.sign_up()
            elif choice == "2":
                self.log_in()
            elif choice == "3":
                print("Exiting Pocket Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")

    def sign_up(self):
        print("\nSign Up:")
        username = input("Enter a username: ")
        if username in self.user_data:
            print("Username already exists. Please try a different username.")
            return
        
        password = input("Enter a password: ")
        self.user_data[username] = {
            'password': password,
            'spending_limit': 0.0,  # Default spending limit
            'amount_spent': 0.0    # Default amount spent
        }
        self.save_user_data()
        print(f"Account created successfully for user: {username}")

    def log_in(self):
        print("\nLog In:")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        user = self.user_data.get(username)
        if user and user['password'] == password:
            print("Login successful!")
            self.logged_in = True
            self.current_user = username
            self.pocket_tracker_menu()
        else:
            print("Incorrect username or password. Please try again.")

    def pocket_tracker_menu(self):
        while self.logged_in:
            print(f"Spending Limit: ${self.user_data[self.current_user]['spending_limit']}")
            print(f"Amount Spent: ${self.user_data[self.current_user]['amount_spent']}")
            print("\nPocket Tracker Menu:")
            print("1. Set Spending Limit")
            print("2. Track Spending")
            print("3. Log Out")
            choice = input("Please select an option: ")

            if choice == "1":
                self.set_spending_limit()
            elif choice == "2":
                self.simulate_spending()
            elif choice == "3":
                print("Logging out...")
                self.logged_in = False
                self.current_user = None
                self.save_user_data()  # Save changes on logout
            else:
                print("Invalid choice. Please select 1, 2, or 3.")

    def set_spending_limit(self):
        try:
            limit = float(input("Set your monthly spending limit: $"))
            self.user_data[self.current_user]['spending_limit'] = limit
            print(f"Monthly spending limit set to ${limit:.2f}")
            self.save_user_data()
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            self.set_spending_limit()

    def simulate_spending(self):
        print("Tracking spending. Enter each spending amount below.")
        while True:
            try:
                spend_amount = float(input("Enter amount spent (or type -1 to return): $"))
                if spend_amount == -1:
                    break
                
                self.user_data[self.current_user]['amount_spent'] += spend_amount
                print(f"Total spending so far: ${self.user_data[self.current_user]['amount_spent']:.2f}")

                if self.user_data[self.current_user]['amount_spent'] >= self.user_data[self.current_user]['spending_limit']:
                    print("Alert: You have reached your spending limit!")
                    break
                elif self.user_data[self.current_user]['amount_spent'] >= 0.8 * self.user_data[self.current_user]['spending_limit']:
                    print("Warning: You have reached 80% of your spending limit.")
                    
                self.save_user_data()
                    
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")

# Run the Pocket Tracker program
if __name__ == "__main__":
    tracker = PocketTracker()
    tracker.display_welcome_message()
    tracker.main_menu()