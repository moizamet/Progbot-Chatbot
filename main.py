#!/home/batman/Environment/dev/bin/python3
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from login import Ui_Login


class chatbot(QtWidgets.QMainWindow, Ui_Login):

	def __init__(self):
		super(chatbot, self).__init__()
		self.setupUi(self)

if __name__ == "__main__":
	app  = QtWidgets.QApplication(sys.argv)
	gui = chatbot()
	gui.show()
	sys.exit(app.exec_())
