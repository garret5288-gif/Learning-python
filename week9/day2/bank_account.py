# A simple bank account manager
# The user can deposit, withdraw, and check balance.

class BankAccount: # BankAccount class to manage account
    def __init__ (self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount): # Deposit money into account
        if amount > 0: # only positive amounts
            self.balance += amount
            print(f"Deposited: ${amount:.2f}")
            print(f"New balance: ${self.balance:.2f}")
        else: # reject non-positive amounts
            print("Deposit amount must be positive.")

    def withdraw(self, amount): # Withdraw money from account
        if 0 < amount <= self.balance: # valid amount and sufficient funds
            self.balance -= amount
            print(f"Withdrew: ${amount:.2f}")
            print(f"New balance: ${self.balance:.2f}")
        else:
            print("Invalid withdrawal amount or insufficient funds.")

    def get_balance(self): # Return current balance
        return self.balance
    
def menu(): # Display menu options
        print("Welcome to the Bank Account Manager")
        print("-------------------------------")
        print("1. Add funds")
        print("2. Withdraw funds")
        print("3. Check balance")
        print("4. Exit")

    
def main(): # Main program loop

    account = BankAccount("User") # Create a bank account for the user
    
    while True: # Loop until user chooses to exit
        menu()
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            raw = input("Enter amount to deposit (press Enter to cancel): ").strip()
            if raw == "": # cancel if empty
                print("Deposit canceled.")
            else: # proceed with deposit
                try:
                    amount = float(raw)
                except ValueError:  # Handle non-numeric input
                    print("Invalid amount. Please enter a number.")
                else:
                    account.deposit(amount)
        elif choice == "2":
            raw = input("Enter amount to withdraw (press Enter to cancel): ").strip()
            if raw == "": # cancel if empty
                print("Withdrawal canceled.")
            else: # proceed with withdrawal
                try:
                    amount = float(raw)
                except ValueError:  # Handle non-numeric input
                    print("Invalid amount. Please enter a number.")
                else:
                    account.withdraw(amount)
        elif choice == "3": # Check balance
            print(f"Current balance: ${account.get_balance():.2f}")
        elif choice == "4": # Exit program
            print("Exiting. Thank you for using the Bank Account Manager.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
