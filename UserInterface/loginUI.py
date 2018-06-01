# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_Form.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from mainWindowUI import Ui_MainWindow
class Ui_Dialog(object):
    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        Dialog.hide()
        self.window.show()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(613, 366)
        self.userDetailsGroup = QtWidgets.QGroupBox(Dialog)
        self.userDetailsGroup.setGeometry(QtCore.QRect(150, 190, 321, 101))
        self.userDetailsGroup.setTitle("")
        self.userDetailsGroup.setObjectName("userDetailsGroup")
        self.label_2 = QtWidgets.QLabel(self.userDetailsGroup)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 51, 20))
        self.label_2.setObjectName("label_2")
        self.userText = QtWidgets.QLineEdit(self.userDetailsGroup)
        self.userText.setGeometry(QtCore.QRect(80, 30, 211, 20))
        self.userText.setObjectName("userText")
        self.passText = QtWidgets.QLineEdit(self.userDetailsGroup)
        self.passText.setEnabled(True)
        self.passText.setGeometry(QtCore.QRect(80, 60, 211, 20))
        self.passText.setMouseTracking(True)
        self.passText.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhSensitiveData)

        self.passText.setObjectName("passText")
        self.label = QtWidgets.QLabel(self.userDetailsGroup)
        self.label.setGeometry(QtCore.QRect(20, 30, 51, 20))
        self.label.setObjectName("label")
        self.label_2.raise_()
        self.userText.raise_()
        self.passText.raise_()
        self.label.raise_()
        self.loginBtn = QtWidgets.QPushButton(Dialog)
        self.loginBtn.setGeometry(QtCore.QRect(270, 310, 75, 23))
        self.loginBtn.setObjectName("loginBtn")
        self.loginBtn.clicked.connect(self.openWindow)


        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setEnabled(False)
        self.textEdit.setGeometry(QtCore.QRect(200, 80, 221, 51))
        self.textEdit.setObjectName("textEdit")
        self.testLabel = QtWidgets.QLabel(Dialog)
        self.testLabel.setGeometry(QtCore.QRect(440, 320, 111, 20))
        self.testLabel.setObjectName("testLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Password"))
        self.label.setText(_translate("Dialog", "Username"))
        self.loginBtn.setText(_translate("Dialog", "Log In"))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:20pt;\">A </span><span style=\" font-size:14pt;\">Silent Voice</span></p></body></html>"))
        self.testLabel.setText(_translate("Dialog", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

