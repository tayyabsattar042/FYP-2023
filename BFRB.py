import json
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
import firebase_auth
from formUi import FormScreen


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("Screens/welcomescreen.ui",self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("Screens/login.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()

        if len(user)==0 or len(password)==0:
            self.error.setText("Please input all fields.")

        else:
            res=firebase_auth.login(user,password)
            if res:
                self.error.setText("")
                print(res)
                self.mainwindow=FormScreen(str(res))
                self.mainwindow.setFixedSize(1200, 800)
                self.mainwindow.show()
                widget.close()
            else:
                self.error.setText("Incorrect email or password")

class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("Screens/createacc.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signupfunction)


    def signupfunction(self):
        name = self.namefield.text()
        user = self.emailfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()

        if len(user)==0 or len(password)==0 or len(confirmpassword)==0 or len(name)==0:
            self.error.setText("Please fill in all inputs.")

        elif password!=confirmpassword:
            self.error.setText("Passwords do not match.")
        else:
            res=firebase_auth.signUp(user,password,name)
            if res=="Successfully Signed Up":
                self.error.setText("Succesfully Signed Up")
                with open('Json/weekly.json','r') as f:
                    data = json.load(f)
                data[str(name)]={}
                with open('Json/weekly.json','w') as f:
                    json.dump(data,f)
                with open('Json/yearly.json','r') as f:
                    data1 = json.load(f)
                data1[str(name)]={"yearly":{}}
                with open('Json/yearly.json','w') as f:
                    json.dump(data1,f)
                self.mainwindow = FormScreen(str(name))
                self.mainwindow.setFixedSize(1200,800)
                self.mainwindow.show()
                widget.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()
    sys.exit(app.exec_())
