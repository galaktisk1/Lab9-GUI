"""
bank_service.py
"""

from accounts_model import Account, SavingAccount

class BankService:
    def __init__(self) -> None:
        """Create a new BankService with an empty account list."""
        self._accounts: list[Account] = []

    def create_account(self, name: str, is_savings: bool, initial_balance: float = 0.0) -> Account:
        """
        Create an Account or SavingAccount, add it to the list, and return it.
        
        name: account holder's name
        is_savings: True for SavingAccount, False for regular Account
        initial_balance: starting balance for the account
        
        Saving accounts always respect their minimum balance.
        """
        if is_savings:
            account = SavingAccount(name)
            # Only raise above the minimum if needed
            if initial_balance > SavingAccount.minimum:
                account.set_balance(initial_balance)
        else:
            account = Account(name, initial_balance)

        self._accounts.append(account)
        return account

    def get_all_accounts(self) -> list[Account]:
        """Return the list of all accounts managed by this BankService."""
        return self._accounts

    def get_bank_total(self) -> float:
        """Return the total balance of all accounts combined."""
        total = 0.0
        for account in self._accounts:
            total += account.get_balance()
        return total 