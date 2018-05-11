
import sys
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from reg import Ui_Register
from chatwindow import chatwindow

class Ui_Login(QtWidgets.QDialog):

	def __init__(self):
		super(Ui_Login, self).__init__()
		self.db_conn = sqlite3.connect('Database/login.db')
		self.db_conn.execute("CREATE TABLE IF NOT EXISTS login (userid TEXT PRIMARY KEY, pass TEXT);")
		self.setupUi(self)

	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(412, 251)
		Dialog.setMinimumSize(QtCore.QSize(412, 251))
		Dialog.setMaximumSize(QtCore.QSize(412, 251))
		self.label = QtWidgets.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(40, 60, 81, 21))
		font = QtGui.QFont()
		font.setFamily("FreeSans")
		font.setPointSize(12)
		self.label.setFont(font)
		self.label.setAutoFillBackground(False)
		self.label.setObjectName("label")
		self.label_2 = QtWidgets.QLabel(Dialog)
		self.label_2.setGeometry(QtCore.QRect(40, 110, 81, 16))
		font = QtGui.QFont()
		font.setFamily("FreeSans")
		font.setPointSize(12)
		self.label_2.setFont(font)
		self.label_2.setObjectName("label_2")
		self.le_username = QtWidgets.QLineEdit(Dialog)
		self.le_username.setGeometry(QtCore.QRect(150, 50, 211, 31))
		self.le_username.setObjectName("le_username")
		self.le_password = QtWidgets.QLineEdit(Dialog)
		self.le_password.setGeometry(QtCore.QRect(150, 100, 211, 31))
		self.le_password.setEchoMode(QtWidgets.QLineEdit.Password)
		self.le_password.setObjectName("le_password")
		self.btn_login = QtWidgets.QPushButton(Dialog)
		self.btn_login.setGeometry(QtCore.QRect(150, 160, 88, 34))
		self.btn_login.setObjectName("btn_login")
		self.btn_cancel = QtWidgets.QPushButton(Dialog)
		self.btn_cancel.setGeometry(QtCore.QRect(270, 160, 88, 34))
		self.btn_cancel.setObjectName("btn_cancel")
		self.btn_newuser = QtWidgets.QPushButton(Dialog)
		self.btn_newuser.setGeometry(QtCore.QRect(40, 160, 88, 34))
		self.btn_newuser.setObjectName("btn_newuser")

		# connect function with newuser button
		self.btn_newuser.clicked.connect(self.newUserRegistration)
		self.btn_cancel.clicked.connect(self.cancel_btn)
		self.btn_login.clicked.connect(self.loginCheck)
		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "Login"))
		self.label.setText(_translate("Dialog", "username"))
		self.label_2.setText(_translate("Dialog", "Password"))
		self.btn_login.setText(_translate("Dialog", "Login"))
		self.btn_cancel.setText(_translate("Dialog", "Cancel"))
		self.btn_newuser.setText(_translate("Dialog", "New User"))


	def newUserRegistration(self):
		self.newUser = Ui_Register(self.db_conn)
		self.newUser.show()

	def cancel_btn(self):
		sys.exit()

	def loginCheck(self):
		self.the_cursor = self.db_conn.cursor()
		getUserName = self.le_username.text()
		getPassword = self.le_password.text()
		if not getUserName:
			QtWidgets.QMessageBox.warning(self, 'Guess What?', 'Username Missing!!!')

		elif not getPassword:
			QtWidgets.QMessageBox.warning(self, 'Guess What?', 'Password Missing!!!')
		else:
			self.sql = "SELECT pass FROM login WHERE userid = '"+getUserName+"'"

			self.the_cursor.execute(self.sql)	
			rs = self.the_cursor.fetchone()
			if rs is None:
				QtWidgets.QMessageBox.warning(self, 'Guess What?', 'Wrong Credentials!!!')
			else:
				if rs[0] == getPassword:
					QtWidgets.QMessageBox.information(self, 'BOOYA', 'Success')
					self.chat_window = chatwindow(getUserName)
					self.chat_window.show()
					self.hide()
				else:
					QtWidgets.QMessageBox.warning(self, 'Guess What?', 'Wrong Credentials')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Login()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

