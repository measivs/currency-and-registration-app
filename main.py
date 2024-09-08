import warnings

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=".*sipPyTypeDict() is deprecated.*"
)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QStackedWidget
from PyQt5.uic import loadUi
import sys, os

HARDCODED_USERNAME = 'admin'
HARDCODED_PASSWORD = 'admin'

currency = {
    'gel to eur': 0.34,
    'eur to gel': 2.97,
    'gel to usd': 0.37,
    'usd to gel': 2.69,
    'eur to usd': 1.11,
    'usd to eur': 0.90
}

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, 'window.ui')
        loadUi(ui_path, self)

        self.username_input = self.findChild(QtWidgets.QLineEdit, "lineEdit") 
        self.password_input = self.findChild(QtWidgets.QLineEdit, "lineEdit_2") 
        self.registration_button = self.findChild(QtWidgets.QPushButton, "pushButton")   

        self.stacked_widget = self.findChild(QStackedWidget, "stackedWidget")
        self.registration_page = self.findChild(QtWidgets.QWidget, "registration")  
        self.currency_page = self.findChild(QtWidgets.QWidget, "currency")  

        self.from_currency = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.to_currency = self.findChild(QtWidgets.QComboBox, "comboBox_2")
        self.amount = self.findChild(QtWidgets.QLineEdit, "lineEdit_3")
        self.convert_button = self.findChild(QtWidgets.QPushButton, "pushButton_3")

        self.logout = self.findChild(QtWidgets.QPushButton, "pushButton_2")

        self.logout.clicked.connect(self.after_logout)
        self.registration_button.clicked.connect(self.verify_credentials)
        self.convert_button.clicked.connect(self.convert_currency)

    def verify_credentials(self):
        entered_username = self.username_input.text()
        entered_password = self.password_input.text()

        if entered_username == HARDCODED_USERNAME and entered_password == HARDCODED_PASSWORD:
            self.stacked_widget.setCurrentWidget(self.currency_page)
        else:
            QMessageBox.warning(self, "ხარვეზი", "გთხოვთ, შეიყვანოთ სწორი მონაცემები!")

    def convert_currency(self):
        try:
            entered_from = self.from_currency.currentText()
            entered_to = self.to_currency.currentText()
            entered_amount = float(self.amount.text())

            if entered_amount <= 0:
                QMessageBox.warning(self, "ხარვეზი", "გთხოვთ, შეიყვანოთ დადებითი რიცხვი!")
                return

            if entered_from == entered_to:
                QMessageBox.warning(self, "ხარვეზი", "იგივე ვალუტაში კონვერტაცია არ ხდება!")
                return
            
            conversion_key = f"{entered_from.lower()} to {entered_to.lower()}"
            if conversion_key in currency:
                converted = round(currency[conversion_key] * entered_amount, 4)
                QMessageBox.information(self, "კონვერტაციის შედეგი", f"კონვერტაციით მიღებული შედეგია: {converted}{entered_to}")
        except ValueError:
            QMessageBox.warning(self, "ხარვეზი", "გთხოვთ, შეიყვანოთ რიცხვები!")

    def after_logout(self):
        self.username_input.clear()
        self.password_input.clear()
        self.from_currency.setCurrentIndex(0)
        self.to_currency.setCurrentIndex(0)
        self.amount.clear()
        self.stacked_widget.setCurrentWidget(self.registration_page)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())
