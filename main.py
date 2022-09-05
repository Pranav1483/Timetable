import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QApplication
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import re
import pandas as pd
import os
import numpy as np
import csv


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.label_4 = None
        self.w = None
        self.label = None
        self.combo = None
        self.options = None
        self.msgBox = None
        self.btn = None
        self.textbox = None
        self.label_3 = None
        self.label_2 = None
        self.label_1 = None
        self.left = 700
        self.top = 300
        self.width = 500
        self.height = 310
        self.title = "Login"
        self.GUIComponents()

    def GUIComponents(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label_1 = QLabel(self)
        self.label_1.setText("Login Page")
        self.label_1.move(170, 10)
        self.label_1.resize(300, 50)
        self.label_1.setFont(QFont("Arial", 20))

        self.label_2 = QLabel(self)
        self.label_2.setText("Username : ")
        self.label_2.resize(250, 50)
        self.label_2.move(100, 100)
        self.label_2.setFont(QFont("Times", 10))

        self.label_3 = QLabel(self)
        self.label_3.setText("Password  :  ")
        self.label_3.move(100, 150)
        self.label_3.setFont(QFont("Times", 10))

        self.label_4 = QLineEdit(self)
        self.label_4.move(200, 110)
        self.label_4.resize(150, 30)
        self.label_4.setFont(QFont("Times", 10))

        self.textbox = QLineEdit(self)
        self.textbox.setEchoMode(QLineEdit.Password)
        self.textbox.move(200, 150)
        self.textbox.resize(150, 30)

        self.btn = QPushButton("Login", self)
        self.btn.setGeometry(200, 220, 90, 30)

        self.btn.clicked.connect(self.on_click)
        self.show()

    def on_click(self):
        username = self.label_4.text()
        password = self.textbox.text()
        return self.process(username, password)

    def process(self, user, pwd):
        def get_text(user, pwd):
            options = Options()
            options.add_argument("--headless")
            browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
            browser.get('https://workflow.iitm.ac.in/student')
            browser.find_element('id', 'txtUserName').send_keys(user)
            browser.find_element('id', 'txtPassword').send_keys(pwd)
            browser.find_element('id', 'Login').click()
            a = browser.find_element('id', 'aspnetForm').text
            print(a)
            browser.close()
            tmp2 = re.search(r'Academic Calander', a)
            tmp1 = re.search(r'Course No Course Name Slot Category Type', a)
            txt = a[tmp1.span()[1]:tmp2.span()[0]]
            tx_list = re.split(r'\s+', txt)
            return tx_list

        def match(tx_list):
            tt = {}
            flag = 0
            key = val = ''
            for i in range(len(tx_list) - 1):
                if flag == 0:
                    if len(tx_list[i]) == 6 and tx_list[i][:2].isalpha() and tx_list[i][2:].isnumeric():
                        val = tx_list[i]
                    elif len(tx_list[i]) == 1 and (
                            tx_list[i + 1] == "Science" or tx_list[i + 1] == "Professional" or tx_list[
                        i + 1] == "Engineering" or
                            tx_list[i + 1] == "Humanities"):
                        key = tx_list[i]
                        flag = 1
                if flag == 1:
                    tt[key] = val
                    flag = 0
            return tt

        def make_tt(tt, user):
            df = pd.read_csv(os.getcwd() + "/Slotwise.csv")
            arr = df.to_numpy()

            for i in range(1, len(arr)):
                for j in range(len(arr[0])):
                    if len(arr[i][j]) == 1 or len(arr[i][j]) == 5:
                        for x in tt.keys():
                            if x in arr[i][j]:
                                arr[i][j] = tt[x]
                                break
            for i in range(1, len(arr)):
                for j in range(len(arr[0])):
                    if len(arr[i][j]) == 1 or len(arr[i][j]) == 5:
                        arr[i][j] = ''
            arr[0][0] = ''

            a = np.array(arr)
            download_folder = os.getcwd() + '/Results/'
            with open(download_folder + user.upper() + '.csv', 'w', newline='') as file:
                mywriter = csv.writer(file, delimiter=',')
                mywriter.writerows(a)

        make_tt(match(get_text(user, pwd)), user)
        self.close()


app = QApplication(sys.argv)
w = Window()
sys.exit(app.exec_())
