"""
accounts_model.py
"""

class Account:
    """
    A basic bank account with deposit and withdrawal functionality.
        _account_name (str): Name of the account owner.
        _account_balance (float): Current account balance.
    """
    
    def __init__(self, name: str, balance: float = 0.0) -> None:
        self._account_name = name
        self.set_balance(balance)

    def deposit(self, amount: float) -> bool:
        """Adds money to the account if the amount is positive."""
        if amount > 0:
            self._account_balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """Withdraws money if the amount is valid and balance is sufficient."""
        if 0 < amount <= self._account_balance:
            self._account_balance -= amount
            return True
        return False

    def get_balance(self) -> float:
        """Returns the current balance."""
        return self._account_balance
    
    def get_name(self) -> str:
        """Returns the account holder's name."""
        return self._account_name

    def set_balance(self, value: float) -> None:
        """Sets the balance, ensuring it is not negative."""
        if value >= 0:
            self._account_balance = value
        else:
            self._account_balance = 0.0

    def set_name(self, value: str) -> None:
        """Updates the account name."""
        self._account_name = value
        
    def __str__(self) -> str:
        """String representation of the account."""
        return f"Account name = {self._account_name}, Account balance = {self._account_balance:.2f}"


class SavingAccount(Account):
    """
    A savings account with a minimum balance and periodic interest.

    Class attributes:
        minimum (float): Minimum allowed balance.
        rate (float): Interest rate applied every 5th deposit.
    """

    minimum: float = 100.0
    rate: float = 0.02

    def __init__(self, name: str) -> None:
        super().__init__(name, SavingAccount.minimum)
        self._deposit_count = 0

    def apply_interest(self) -> None:
        """Applies interest based on the current balance."""
        interest = self.get_balance() * SavingAccount.rate
        self.set_balance(self.get_balance() + interest)

    def deposit(self, amount: float) -> bool:
        """Deposit with interest applied every 5th deposit."""
        if amount > 0:
            super().deposit(amount)
            self._deposit_count += 1
            if self._deposit_count % 5 == 0:
                self.apply_interest()
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """Withdraw only if the minimum balance is maintained."""
        if amount > 0 and (self.get_balance() - amount) >= SavingAccount.minimum:
            super().withdraw(amount)
            return True
        return False

    def set_balance(self, value: float) -> None:
        """Ensures the balance never drops below the minimum."""
        if value < SavingAccount.minimum:
            super().set_balance(SavingAccount.minimum)
        else:
            super().set_balance(value)

    def __str__(self) -> str:
        """String representation of the savings account."""
        return f"SAVING ACCOUNT: Account name = {self.get_name()}, Account balance = {self.get_balance():.2f}"