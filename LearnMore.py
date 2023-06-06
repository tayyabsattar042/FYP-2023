import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi


class HelpDialog(QDialog):
    def __init__(self):
        super(HelpDialog, self).__init__()
        loadUi("Screens/learnmore.ui", self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = HelpDialog()
    dialog.setFixedSize(835,695)
    dialog.show()
    sys.exit(app.exec_())
