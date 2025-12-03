"""
storage_accounts.py

Loads accounts from a CSV file and saves them back to a CSV file.
Works together with BankService, which holds the actual Account objects.

The CSV format uses three columns:
    name, account_type, balance

Account types are written as "ACCOUNT" or "SAVINGS".
"""

import csv
from accounts_model import Account, SavingAccount
from bank_service import BankService


def load_accounts_from_csv(file_path, service):
    """
    Load accounts from a CSV file and add them to the BankService.

    - If the file does not exist, nothing happens.
    - Bad rows are skipped silently.
    """
    try:
        f = open(file_path, "r", newline="")
    except FileNotFoundError:
        return

    with f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("name") or "").strip()
            acct_type = (row.get("account_type") or "").strip()
            balance_text = (row.get("balance") or "0").strip()

            if name == "":
                continue

            try:
                balance = float(balance_text)
            except ValueError:
                continue

            if acct_type.upper() == "SAVINGS":
                service.create_account(name, True, balance)
            else:
                service.create_account(name, False, balance)


def save_accounts_to_csv(file_path, service):
    """
    Write all accounts from the BankService into a CSV file.

    - Overwrites any existing file.
    - Fails silently if the file cannot be written.
    """
    try:
        f = open(file_path, "w", newline="")
    except Exception:
        return

    with f:
        fieldnames = ["name", "account_type", "balance"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for account in service.get_all_accounts():
            if isinstance(account, SavingAccount):
                acct_type = "SAVINGS"
            else:
                acct_type = "ACCOUNT"

            writer.writerow({
                "name": account.get_name(),
                "account_type": acct_type,
                "balance": "%.2f" % account.get_balance()
            })