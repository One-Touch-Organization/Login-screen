import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QLineEdit
from PyQt5.uic import loadUi
import sqlite3 as sql
from PyQt5.QtGui import QIcon

class Login(QDialog): #окно войти
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction) #Подключаю кнопку к функции логин
        self.registerbutton.clicked.connect(self.gotocreate) #Подключаю кнопку к функции гоутукриейт
        self.hidebutton.clicked.connect(self.hidepassword)

    def loginfunction(self):
        email=self.email.text()  #переменная емейл будет равна тексту в поле емейл
        password = self.password.text() # тоже самое но пароль

        if len(email) == 0 or len(password) == 0 :
            self.errorla.setText("Не всі поля заповнені")

        else:
            conn = sql.connect('accounts.db')
            cur = conn.cursor()
            kil = 'SELECT password FROM users WHERE email = \''+email+"\'" #по емейлу дивимося пароль в базі
            cur.execute(kil)
            myresult = cur.fetchone()[0]# переменная стает равна значению выше как числу
            if myresult == password:# проверка равности пароля в базе и ввденому паролю
                self.mainwindow = Mainwindow()
                self.mainwindow.show()
                widget.close()
            else:
                self.errorla.setText("Неправильний логін або пароль")
            conn.close()

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)# переключает окна

    def hidepassword(self):
        if self.password.echoMode() == QLineEdit.Normal:
            self.password.setEchoMode(QLineEdit.Password)# пароль выиглядає як *
        else:
            self.password.setEchoMode(QLineEdit.Normal)#нормальный пароль






class CreateAcc(QDialog): #окно регистрации
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createaccount.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)#Подключаю кнопку к функции createaccfun..
        self.goinbutton.clicked.connect(self.goinfunction)

    def createaccfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()

        if len(user) == 0 or len(password) == 0 or len(confirmpassword) == 0 :
            self.errorla.setText("Не всі поля заповнені")
        elif password != confirmpassword :
            self.errorla.setText("Паролі не одинакові")
        else:
            conn = sql.connect('accounts.db')#подключаюсь до бази
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM users WHERE email=?', (user,))
            checkUsername = cur.fetchone()[0]
            if checkUsername == 0:
                user_info = [user, password]
                cur.execute('INSERT INTO users (email, password) VALUES (?,?)', user_info)#записує в базу юзерив емейл и пароль

                conn.commit()#підтверджую завершення виконання строчки више
                conn.close()#припиняю роботу бази даних

                goin = Login()
                widget.addWidget(goin)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                self.errorla.setText('Такий юзер уже існуе')




    def goinfunction(self):
        goin = Login()
        widget.addWidget(goin)
        widget.setCurrentIndex(widget.currentIndex()+1)# переключает окна

class Mainwindow(QMainWindow): #окно регестрации
    def __init__(self):
        super(Mainwindow,self).__init__()
        loadUi("mainwindow.ui",self)
        self.setWindowTitle("Бимбам")

#main

app=QApplication(sys.argv)

mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("Вхід в програму")#назва сверху
widget.setWindowIcon(QIcon('logo.png'))#иконка
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()