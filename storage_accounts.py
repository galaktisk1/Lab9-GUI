"""
storage_accounts.py
"""

import csv
from accounts_model import SavingAccount
from bank_service import BankService

def load_accounts_from_csv(file_path: str, service: BankService) -> None:
    """
    Load accounts from a CSV file and add them to the BankService.
    If the file does not exist, nothing happens.
    Bad rows are skipped silently.
    """
    try:
        f = open(file_path, "r", newline="")
    except FileNotFoundError:
        return

    with f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header row
        for row in reader:
            if len(row) != 3:
                continue
            name: str
            acct_type: str
            balance_str: str
            name, acct_type, balance_str = row
            try:
                balance: float = float(balance_str)
            except ValueError:
                continue

            if acct_type == "SAVINGS":
                is_savings = True
            elif acct_type == "CHECKING":
                is_savings = False
            else:
                continue

            service.create_account(name, is_savings, balance)

def save_accounts_to_csv(file_path: str, service: BankService) -> None:
    """
    Write all accounts from the BankService into a csv file.
    Overwrites any existing file.
    Fails silently if the file cannot be written.
    """
    try:
        f = open(file_path, "w", newline="")
    except Exception:
        return

    with f:
        writer = csv.writer(f)
        writer.writerow(["name", "account_type", "balance"])
        accounts = service.get_all_accounts()
        for account in accounts:
            acct_type: str = "SAVINGS" if isinstance(account, SavingAccount) else "CHECKING"
            writer.writerow([account.get_name(), acct_type, f"{account.get_balance():.2f}"])