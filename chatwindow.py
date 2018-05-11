import os
import aiml
import sys
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

class chatwindow(QtWidgets.QMainWindow):

    def __init__(self, userName):
        super(chatwindow, self).__init__()
        self.userName = userName

        self.db = sqlite3.connect("Database/quiz.db")
        self.cur = self.db.cursor()

        self.kernel = aiml.Kernel()
        if os.path.isfile('Resources/bot_brain.brn'):
            self.kernel.bootstrap(brainFile='Resources/bot_brain.brn')
        else:
            self.kernel.learn('std-startup.xml')
            self.kernel.respond("programming")
            self.kernel.saveBrain('Resources/bot_brain.brn')


        # create 2 QListWidgetItem one for user & bot
        # create 3rd item for user query
        self.userMdl = QtWidgets.QListWidgetItem("User")
        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setPointSize(10)

        self.brush = QtGui.QBrush()
        self.brush.setColor(QtGui.QColor(255, 0, 0, 255))

        self.userMdl.setFont(self.font)
        self.userMdl.setForeground(self.brush)
        self.userMdl.setTextAlignment(3)

        self.botMdl = QtWidgets.QListWidgetItem("Bot")
        self.brush.setColor(QtGui.QColor(0, 0, 255, 255))
        self.botMdl.setFont(self.font)
        self.botMdl.setForeground(self.brush)

        self.usrMessage = QtWidgets.QListWidgetItem()
        self.usrMessage.setTextAlignment(3)

        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(591, 432)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.send = QtWidgets.QPushButton(self.centralwidget)
        self.send.setObjectName("send")
        self.gridLayout.addWidget(self.send, 2, 1, 1, 1)
        self.chatbox = QtWidgets.QListWidget(self.centralwidget)
        self.chatbox.setObjectName("chatbox")
        self.gridLayout.addWidget(self.chatbox, 0, 0, 2, 2)
        self.message = QtWidgets.QLineEdit(self.centralwidget)
        self.message.setObjectName("message")
        self.gridLayout.addWidget(self.message, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 591, 30))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionManual = QtWidgets.QAction(MainWindow)
        self.actionManual.setObjectName("actionManual")

        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout_us = QtWidgets.QAction(MainWindow)
        self.actionAbout_us.setObjectName("actionAbout_us")


        self.actionExit.triggered.connect(self.close_application)
        self.actionClear.triggered.connect(self.clear_window)
        self.send.clicked.connect(self.chat)
        self.actionAbout_us.triggered.connect(self.about_us)
        self.actionManual.triggered.connect(self.manual)
        self.chatbox.setWordWrap(True)


        self.chatbox.addItem(QtWidgets.QListWidgetItem(self.botMdl))
        self.chatbox.addItem("Welcome")



        self.menuOptions.addAction(self.actionClear)
        self.menuOptions.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionManual)
        self.menuHelp.addAction(self.actionAbout_us)
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def about_us(self):
        QtWidgets.QMessageBox.information(self,'About ProgBot', 'ProgBot is your new friend to teach programming language. ProgBot is programmed to teach Java in an efficient and effective manner and makes it hassle free for begineers. Any queries can be asked to the progbot and receive instant answer. Just follow the user manual from the help menu on how to use ProgBot.\n\n Designed by Moiz Amet and Amitava')

    def manual(self):
        QtWidgets.QMessageBox.information(self,'User Manual', 
            'Follow these instruction when using the bot:\n'+
            '1. What is [question] ?\n'+
            '2. Define [anything] or simply [anything]\n'+
            '3. For contineous chat type example to see example and type more to see more concepts about that topic\n'+
            '4. Type quiz to see the list of quiz\n'+
            '5. Start [quiz no] to take quiz of following lession\n'+
            '6. Once in quiz mode type exit to exit from quiz mode\n'+
            '7. Be careful of your spelling mistake, ProgBot doesnt like it\n'+
            '8. To see this manual type manual or go to help --> manual')

    def read_From_db(self):
        self.cur.execute('SELECT * FROM questions where quiz_id = ?', (self.quizId,))

        self.questions = self.cur.fetchall()

        self.total_questions = len(self.questions)
        self.index = 0
        self.score = 0



    def update_score(self):
        self.cur.execute('UPDATE score SET score=? AND quiz_id=? WHERE user_id=?', (self.score, self.quizId, self.userName))
        self.db.commit()


    def conduct_quiz(self):
        
        # check answer of 1st question
        self.getMessage = self.message.text()
        self.chatbox.addItem(QtWidgets.QListWidgetItem(self.userMdl))
        self.usrMessage.setText(self.getMessage)
        self.chatbox.addItem(QtWidgets.QListWidgetItem(self.usrMessage))
        self.message.clear()

        if self.getMessage == "exit":
            self.send.clicked.connect(self.chat)
            self.send.clicked.disconnect(self.conduct_quiz)
            self.update_score()
            self.questions = None
            self.total_questions = 0
            return

        # update score accordingly
        self.chatbox.addItem(QtWidgets.QListWidgetItem(self.botMdl))
        if int(self.getMessage) == self.answer:
            self.chatbox.addItem("Correct Answer")
            self.score = self.score + 1
        else:
            text = "Wrong answer, correct answer is " + str(self.answer)
            self.chatbox.addItem(text)


        # fetch next question only 10 questions
        if self.index < self.total_questions and self.index < 10:

            self.chatbox.addItem(QtWidgets.QListWidgetItem(self.botMdl))
            self.chatbox.addItem( (self.questions[self.index])[2] )
            self.chatbox.addItem( "1. "+(self.questions[self.index])[3] )
            self.chatbox.addItem( "2. "+(self.questions[self.index])[4] )
            self.chatbox.addItem( "3. "+(self.questions[self.index])[5] )
            self.chatbox.addItem( "4. "+(self.questions[self.index])[6] )
            self.answer = (self.questions[self.index])[7]
            self.index += 1




    def chat(self):

        # copy const.
        
        self.getMessage = self.message.text()
        self.message.clear()        # clearing the messagebox

        self.chatbox.addItem(QtWidgets.QListWidgetItem(self.userMdl))
        self.usrMessage.setText(self.getMessage)
        self.chatbox.addItem(QtWidgets.QListWidgetItem(self.usrMessage))

        self.getResponse = self.kernel.respond(self.getMessage)
        botResponse = self.getResponse.split("-, ")

        self.chatbox.addItem(QtWidgets.QListWidgetItem(self.botMdl))
        if self.getResponse:

            str = ""
            for lines in botResponse:
                str += lines + "\n"

            self.chatbox.addItem(str)

        


        # QUIZ part

        elif self.getMessage.startswith('start'):
            self.send.clicked.disconnect(self.chat)
            self.send.clicked.connect(self.conduct_quiz)

            self.quizId = self.getMessage.split(' ')[1]
            self.read_From_db() 

            # read the first question
            if self.index < self.total_questions:

                
                self.chatbox.addItem( (self.questions[self.index])[2] )
                self.chatbox.addItem( "1. "+(self.questions[self.index])[3] )
                self.chatbox.addItem( "2. "+(self.questions[self.index])[4] )
                self.chatbox.addItem( "3. "+(self.questions[self.index])[5] )
                self.chatbox.addItem( "4. "+(self.questions[self.index])[6] )
                self.answer = (self.questions[self.index])[7]
                self.index += 1

        else:
            self.chatbox.addItem("Can you explain in another way?")
            


    def close_application(self):
        sys.exit()

    def clear_window(self):
        self.chatbox.clear()
        self.message.clear()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chatbot"))
        self.send.setText(_translate("MainWindow", "Send"))
        self.menuOptions.setTitle(_translate("MainWindow", "Opt&ions"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout_us.setText(_translate("MainWindow", "About ProgBot"))
        self.actionManual.setText(_translate("MainWindow", "Manual"))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = chatwindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

