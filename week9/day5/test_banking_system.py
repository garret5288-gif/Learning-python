import os
import sys
from io import StringIO
from contextlib import redirect_stdout

from banking_system import BankingSystem, view_transactions

TEST_DB = os.path.join(os.path.dirname(__file__), "customers_test.json")


def reset_test_db():
    try:
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
    except OSError:
        pass


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def check(self, condition, label):
        if condition:
            self.passed += 1
            print(f"[PASS] {label}")
        else:
            self.failed += 1
            print(f"[FAIL] {label}")

    def summary(self):
        print(f"\nSummary: {self.passed} passed, {self.failed} failed")
        return self.failed == 0


def main():
    t = TestRunner()

    # Fresh DB
    reset_test_db()
    bank = BankingSystem(storage_path=TEST_DB)
    t.check(isinstance(bank.customers, list) and len(bank.customers) == 0, "fresh system starts empty")

    # Create customer
    alice = bank.get_or_create_customer("Alice")
    t.check(alice.name == "Alice", "created customer name correct")
    t.check(alice.account.get_balance() == 0.0, "new customer balance is 0")
    t.check(alice.account.transactions == [], "new customer has no transactions")

    # Deposit edge cases
    t.check(alice.account.deposit(0) is False, "deposit 0 rejected")
    t.check(alice.account.deposit(-5) is False, "deposit negative rejected")
    t.check(alice.account.deposit(float('nan')) is False, "deposit NaN rejected")
    t.check(alice.account.deposit(float('inf')) is False, "deposit +inf rejected")

    # Valid deposit
    t.check(alice.account.deposit(100.0) is True, "deposit 100 accepted")
    t.check(abs(alice.account.get_balance() - 100.0) < 1e-9, "balance updated to 100")
    t.check(len(alice.account.transactions) == 1 and alice.account.transactions[-1]["type"] == "deposit", "transaction recorded for deposit")

    # Withdraw edge cases
    t.check(alice.account.withdraw(0) is False, "withdraw 0 rejected")
    t.check(alice.account.withdraw(-5) is False, "withdraw negative rejected")
    t.check(alice.account.withdraw(float('nan')) is False, "withdraw NaN rejected")
    t.check(alice.account.withdraw(float('inf')) is False, "withdraw +inf rejected")
    t.check(alice.account.withdraw(150) is False, "withdraw over balance rejected")

    # Valid withdraw
    t.check(alice.account.withdraw(40) is True, "withdraw 40 accepted")
    t.check(abs(alice.account.get_balance() - 60.0) < 1e-9, "balance updated to 60")
    t.check(len(alice.account.transactions) == 2 and alice.account.transactions[-1]["type"] == "withdraw", "transaction recorded for withdraw")

    # Persist and reload
    bank.save_customers()
    bank2 = BankingSystem(storage_path=TEST_DB)
    alice2 = bank2.find_customer("alice")
    t.check(alice2 is not None, "case-insensitive customer lookup works after reload")
    t.check(abs(alice2.account.get_balance() - 60.0) < 1e-9, "balance persisted across reload")
    t.check(len(alice2.account.transactions) == 2, "transactions persisted across reload")

    # Add another user and verify both persist
    bob = bank2.get_or_create_customer("Bob")
    t.check(bob.account.deposit(10) is True, "bob deposit works")
    bank2.save_customers()
    bank3 = BankingSystem(storage_path=TEST_DB)
    names = sorted([c.name for c in bank3.customers])
    t.check(names == ["Alice", "Bob"], "multiple customers persisted")

    # Additional edge cases
    # 1) Many tiny increments sum stability
    tiny_ok = True
    for _ in range(1000):
        if not alice2.account.deposit(0.01):
            tiny_ok = False
            break
    t.check(tiny_ok, "tiny deposits accepted repeatedly")
    expected = 60.0 + 1000 * 0.01
    t.check(abs(alice2.account.get_balance() - expected) < 1e-6, "balance correct after many tiny deposits")

    # 2) Very large amount
    t.check(bob.account.deposit(1e12) is True, "very large deposit accepted")
    t.check(bob.account.withdraw(1e12) is True, "very large withdraw accepted if covered")

    # 3) Exact-balance withdraw
    start = alice2.account.get_balance()
    t.check(alice2.account.withdraw(start) is True, "withdraw exact balance to zero")
    t.check(abs(alice2.account.get_balance()) < 1e-9, "balance is zero after exact withdraw")

    # 4) Numeric strings accepted by API (float-cast inside methods)
    t.check(alice2.account.deposit("10") is True, "string amount accepted at API level")
    t.check(abs(alice2.account.get_balance() - 10.0) < 1e-9, "balance updated by string amount")

    # 5) Negative zero
    t.check(alice2.account.deposit(-0.0) is False, "-0.0 treated as non-positive")

    # 6) Non-floatable string should raise at API level
    raised = False
    try:
        alice2.account.deposit("ten")
    except Exception:
        raised = True
    t.check(raised, "non-floatable string raises error at API level")

    # 7) view_transactions shows only last 20 lines
    # Make 25 more $1 deposits so last 20 are all $1 deposits
    for _ in range(25):
        alice2.account.deposit(1)
    buf = StringIO()
    with redirect_stdout(buf):
        view_transactions(alice2.account)
    out = buf.getvalue().strip().splitlines()
    # Count lines starting with '- '
    hyphen_lines = [ln for ln in out if ln.strip().startswith('- ')]
    t.check(len(hyphen_lines) == 20, "view shows last 20 transactions")
    # All last lines should be deposits of $1.00
    t.check(all('deposit' in ln and '$1.00' in ln for ln in hyphen_lines), "view last 20 are recent $1 deposits")

    ok = t.summary()

    # Cleanup
    reset_test_db()

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
