

import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Register(QtWidgets.QDialog):
    def __init__(self, db_conn):
        super(Ui_Register, self).__init__()
        self.db_conn = db_conn
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(419, 251)
        Dialog.setModal(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(419, 251))
        Dialog.setMaximumSize(QtCore.QSize(419, 251))
        Dialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.le_username = QtWidgets.QLineEdit(Dialog)
        self.le_username.setGeometry(QtCore.QRect(150, 50, 211, 31))
        self.le_username.setObjectName("le_username")
        self.btn_back = QtWidgets.QPushButton(Dialog)
        self.btn_back.setGeometry(QtCore.QRect(270, 160, 88, 34))
        self.btn_back.setObjectName("btn_back")
        self.le_password = QtWidgets.QLineEdit(Dialog)
        self.le_password.setGeometry(QtCore.QRect(150, 100, 211, 31))
        self.le_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.le_password.setObjectName("le_password")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 110, 81, 16))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 60, 81, 21))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        self.btn_add = QtWidgets.QPushButton(Dialog)
        self.btn_add.setGeometry(QtCore.QRect(150, 160, 88, 34))
        self.btn_add.setObjectName("btn_add")

        self.btn_back.clicked.connect(self.back_btn)
        self.btn_add.clicked.connect(self.addNewUser)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "New User Registration"))
        self.btn_back.setText(_translate("Dialog", "Cancel"))
        self.label_2.setText(_translate("Dialog", "Password"))
        self.label.setText(_translate("Dialog", "username"))
        self.btn_add.setText(_translate("Dialog", "Add"))

    def back_btn(self):
        self.close()

    def addNewUser(self):
        getUserName = self.le_username.text()
        getPassword = self.le_password.text()
        sql = "INSERT INTO login VALUES ('"+getUserName+"','"+getPassword+"');"
        theCursor = self.db_conn.cursor()
        theCursor.execute("SELECT count(*) FROM login WHERE userid = '"+getUserName+"'")
        rs = theCursor.fetchone()[0]

        if rs > 0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'username already taken')
        else:
            self.db_conn.execute(sql);
            QtWidgets.QMessageBox.information(self, 'Awesome', 'user added successfully')
            self.db_conn.commit();
            
