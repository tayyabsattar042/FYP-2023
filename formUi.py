import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication
from LogUi import LogScreen as LS

import detecttheperson

from LearnMore import HelpDialog
class FormScreen(QDialog):
    def __init__(self,name):
        super(FormScreen, self).__init__()
        loadUi("Screens/form.ui",self)
        self.name=name
        self.username.setText(self.name)
        self.btnexit.clicked.connect(self.exitWindow)
        self.btnlm.clicked.connect(self.LearnMore)
        self.btnstart.clicked.connect(self.run_detection)
        self.btnlog.clicked.connect(self.show_new_window)

    def exitWindow(self):  # Method to exit the application
        QApplication.quit()

    def run_detection(self):
        detecttheperson.run_nail_biting_detection(self.name)

    def show_new_window(self):
        self.stack_window = LS(self.name)
        self.stack_window.setFixedSize(1100,800)
        self.stack_window.show()
    def LearnMore(self):
        self.learnWindow=HelpDialog()
        self.learnWindow.setFixedSize(835,595)
        self.learnWindow.show()

    def closeEvent(self, event):  # If Log window is opened, I cannot close the parent window
        if self.stack_window and self.stack_window.isVisible():
            event.ignore()
        else:
            event.accept()
if __name__=='__main__':

    app = QApplication(sys.argv)
    window=FormScreen()
    window.setFixedSize(1200, 800)
    window.show()
    app.exec()