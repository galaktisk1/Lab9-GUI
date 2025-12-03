from PyQt6.QtWidgets import QMainWindow

from ui_main_gui import Ui_MainWindow
from bank_service import BankService
from storage_accounts import load_accounts_from_csv, save_accounts_to_csv
from accounts_model import SavingAccount

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("BankApp")

        self.bank_service = BankService()
        load_accounts_from_csv("accounts.csv", self.bank_service)

        self.radioRegular.setChecked(True)

        self.refresh_account_dropdown()
        self.setup_connections()
        self.update_selected_account_info()
    
    def setup_connections(self):
        self.comboAccounts.currentIndexChanged.connect(self.account_selected)
        self.buttonCreateAccount.clicked.connect(self.create_account_clicked)
        self.buttonDeposit.clicked.connect(self.deposit_clicked)
        self.buttonWithdraw.clicked.connect(self.withdraw_clicked)

    def refresh_account_dropdown(self):
        self.comboAccounts.clear()
        for account in self.bank_service.get_all_accounts():
            self.comboAccounts.addItem(account.get_name())
    
    def get_selected_account(self):
        index = self.comboAccounts.currentIndex()
        accounts = self.bank_service.get_all_accounts()
        if 0 <= index < len(accounts):
            return accounts[index]
        return None
    
    def update_selected_account_info(self):
        account = self.get_selected_account()
        if account:
            self.labelBalanceValue.setText(f"{account.get_balance():.2f}")
            if isinstance(account, SavingAccount):
                self.labelAccountType.setText("Savings")
            else:
                self.labelAccountType.setText("Regular")
        else:
            self.labelBalanceValue.setText("0.00")
            self.labelAccountType.setText("N/A")
    
    def account_selected(self):
        self.update_selected_account_info()
    
    def create_account_clicked(self):
        name = self.editNewName.text().strip()
        initial_balance_text = self.editInitialBalance.text().strip()
        is_savings = self.radioSavings.isChecked()

        if not name:
            self.labelStatus.setText("Account name cannot be empty.")
            return

        try:
            initial_balance = float(initial_balance_text) if initial_balance_text else 0.0
        except ValueError:
            self.labelStatus.setText("Initial balance must be a valid number.")
            return

        self.bank_service.create_account(name, is_savings, initial_balance)
        self.refresh_account_dropdown()
        self.comboAccounts.setCurrentIndex(self.comboAccounts.count() - 1)
        self.update_selected_account_info()
        self.editNewName.clear()
        self.editInitialBalance.clear()
        self.labelStatus.setText("Account created.")
        
    
    def deposit_clicked(self):
        account = self.get_selected_account()
        if not account:
            self.labelStatus.setText("No account selected.")
            return

        amount_text = self.editAmount.text().strip()
        try:
            amount = float(amount_text)
        except ValueError:
            self.labelStatus.setText("Deposit amount must be a valid number.")
            return

        if account.deposit(amount):
            self.labelStatus.setText("Deposit successful.")
        else:
            self.labelStatus.setText("Deposit failed. Amount must be positive.")

        self.update_selected_account_info()
        self.editAmount.clear()
    
    def withdraw_clicked(self):
        account = self.get_selected_account()
        if not account:
            self.labelStatus.setText("No account selected.")
            return

        amount_text = self.editAmount.text().strip()
        try:
            amount = float(amount_text)
        except ValueError:
            self.labelStatus.setText("Withdraw amount must be a valid number.")
            return

        if account.withdraw(amount):
            self.labelStatus.setText("Withdraw successful.")
        else:
            self.labelStatus.setText("Withdraw failed. Check amount and balance.")

        self.update_selected_account_info()
        self.editAmount.clear()
    
    def closeEvent(self, event):
        save_accounts_to_csv("accounts.csv", self.bank_service)
        event.accept()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())