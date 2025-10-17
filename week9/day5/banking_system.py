import json # JSON storage
# Banking system with customer accounts, deposits, withdrawals, and transaction history.

class Customer: # Class to hold customer information
    def __init__(self, name: str, balance: float = 0.0, transactions=None):
        self.name = name
        self.account = Account(account_name=name, balance=float(balance))
        # Backward/forward compatible transaction restore
        if transactions and isinstance(transactions, list):
            self.account.transactions = transactions

    def get_info(self) -> str: # Display customer info
        return f"Customer: {self.name}, Balance: ${self.account.get_balance():.2f}"


class BankingSystem: # Class to manage multiple customers
    def __init__(self, storage_path: str = "customers.json"):
        self.storage_path = storage_path
        self.customers = self.load_customers()

    def load_customers(self): # Load customers from JSON file
        try: # ensure file operations are safe
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            customers = [] # list of Customer objects
            for item in data if isinstance(data, list) else []:
                name = str(item.get("name", "")).strip()
                balance = float(item.get("balance", 0))
                transactions = item.get("transactions", [])
                customers.append(Customer(name, balance, transactions))
            return customers # return list of customers
        except (OSError, json.JSONDecodeError):
            return []

    def save_customers(self): # Save customers to JSON file
        try: # ensure file operations are safe
            data = [
                {
                    "name": c.name,
                    "balance": c.account.get_balance(),
                    "transactions": c.account.transactions,
                }
                for c in self.customers
            ]
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as e: # handle file errors
            print(f"Error saving customers: {e}")
            return False # indicate failure
        return True # indicate success

    def find_customer(self, name: str): # Find customer by name
        name = (name or "").strip() # sanitize input
        for c in self.customers:  # Iterate through customers
            if c.name.lower() == name.lower():
                return c # found
        return None # not found

    def get_or_create_customer(self, name: str) -> Customer: # Get existing or create new customer
        c = self.find_customer(name)
        if c: # found
            return c
        c = Customer(name=name, balance=0.0)
        self.customers.append(c)
        self.save_customers()
        print(f"Created new customer: {name}")
        return c


class Account: # Class to hold account information
    def __init__(self, account_name: str, balance: float = 0.0):
        self.account_name = account_name
        self.balance = float(balance)
        self.transactions = []  # list of {type, amount, balance}

    def deposit(self, amount: float): # Deposit amount
        amt = float(amount)
        # Reject NaN or Infinity to keep balances valid
        if amt != amt or amt == float('inf') or amt == -float('inf'):
            print("Amount must be a finite number.")
            return False
        if amt <= 0:
            print("Amount must be positive.")
            return False # exit on invalid amount
        self.balance += amt # add to balance
        self.transactions.append({"type": "deposit", "amount": amt, "balance": self.balance})
        return True

    def withdraw(self, amount: float): # Withdraw amount
        amt = float(amount)
        # Reject NaN or Infinity to keep balances valid
        if amt != amt or amt == float('inf') or amt == -float('inf'):
            print("Amount must be a finite number.")
            return False
        if amt <= 0: # Check for valid amount
            print("Amount must be positive.")
            return False
        if amt > self.balance: # Check for sufficient funds
            print("Insufficient funds")
            return False
        self.balance -= amt # deduct from balance
        self.transactions.append({"type": "withdraw", "amount": amt, "balance": self.balance})
        return True

    def get_balance(self) -> float: # Get current balance
        return self.balance

    def transaction(self, amount: float, transaction_type: str): # Perform a transaction
        if transaction_type == "deposit":
            return self.deposit(amount)
        elif transaction_type == "withdraw":
            return self.withdraw(amount)
        else:
            print("Invalid transaction type")
            return False

def view_transactions(account: Account): # View recent transactions
    if not account.transactions: # no transactions
        print("No transactions yet.")
        return
    print("\nRecent Transactions:")
    for t in account.transactions[-20:]:  # show last 20
        ttype = t.get("type", "?")
        amt = t.get("amount", 0.0)
        bal = t.get("balance", 0.0)
        print(f"- {ttype:9} ${amt:,.2f} -> balance ${bal:,.2f}")

def menu(): # Display main menu
    print("===Banking System===")
    print("1. Login or create an account")
    print("2. Customers")
    print("3. Exit")
    print("====================")

def account_menu(): # Display account menu
    print("===Account Menu===")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Check Balance")
    print("4. Transactions")
    print("5. Save & Exit")
    print("==================")

def handle_account_session(customer: Customer, banking_system: BankingSystem): # Handle account session
    acct = customer.account
    while True: # Account session loop
        account_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            val = input("Amount to deposit: ").strip()
            try:
                amount = float(val)
            except ValueError: # Handle invalid input
                print("Please enter a valid number.")
                continue
            if acct.deposit(amount): # Successful deposit
                banking_system.save_customers() # Save after deposit
                print(f"Deposited ${amount:,.2f}.")
        elif choice == "2":
            val = input("Amount to withdraw: ").strip()
            try:
                amount = float(val)
            except ValueError:
                print("Please enter a valid number.")
                continue
            if acct.withdraw(amount): # Successful withdrawal
                banking_system.save_customers() # Save after withdrawal
                print(f"Withdrew ${amount:,.2f}.")
        elif choice == "3":
            print(f"Balance: ${acct.get_balance():,.2f}")
        elif choice == "4":
            view_transactions(acct)
        elif choice == "5":
            banking_system.save_customers()
            print("Saved. Returning to main menu.")
            break
        else:
            print("Invalid choice. Please try again.")

def main(): # Main program loop
    banking_system = BankingSystem() # Initialize banking system
    while True:
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            name = input("Enter your name or create a new account: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            customer = banking_system.get_or_create_customer(name)
            handle_account_session(customer, banking_system)
        elif choice == "2":
            print("Customers:")
            for customer in banking_system.customers:
                print(customer.get_info())
        elif choice == "3":
            print("Exiting Banking System.")
            banking_system.save_customers()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
