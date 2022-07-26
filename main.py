from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit
import sys
import webbrowser
import time
import pyautogui as pg
from nltk.tokenize import word_tokenize
import re
import pandas as pd
import numpy as np
import csv
import os
import subprocess


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
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
        self.title = "TimeTable"
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
        def clrscr():
            clear = lambda: os.system("cls")
            clear()
        
        def workflow():
            url = "https://workflow.iitm.ac.in/"
            webbrowser.register('firefox', None, webbrowser.BackgroundBrowser("C:/Program Files/Mozilla Firefox/firefox.exe"))
            webbrowser.get('firefox').open(url)


        def access(username, password):
            width, height = pg.size()
            time.sleep(3)
            pg.click(width/2, height/4)
            pg.write(username)
            pg.click(width/2, height/2.9)
            pg.write(password)
            pg.click(width/1.8, height/2.4)


        def portal(username, password):
            width, height = pg.size()
            time.sleep(2)
            pg.click(width/3.5, height/1.78)
            time.sleep(3)
            pg.click(width/2, height/2.3)
            pg.write(username)
            pg.click(width/2, height/1.76)
            pg.write(password)
            pg.click(width/1.8, height/1.5)


        def copy():
            time.sleep(4)
            w, h = pg.size()

            pg.moveTo(w/3.6, h/1.8)
            pg.dragTo(w/1.35, h/1.1, 0.5, button='left')
            with pg.hold('ctrl'):
                pg.press('c')
            subprocess.Popen("C:/Windows/notepad.exe")
            time.sleep(1)
            w, h = pg.size()
            pg.click(w/4, h/3, button="right")
            pg.click(w/3.8, h/2.4)
            with pg.hold('ctrl'):
                pg.press('s')
            pg.write("tt")
            pg.press('enter')
            pg.press(['left', 'enter'])


        clrscr()
        workflow()
        access(user, pwd)
        portal(user, pwd)
        copy()

        file = open("E:/Code/Python/Testing/tt.txt", 'r')
        tx = file.read()

        tx_list = word_tokenize(re.sub(r"[^A-Za-z\d]", " ", tx))

        tt = {}
        flag = 0
        for i in range(len(tx_list)-1):
            if flag == 0:    
                if len(tx_list[i]) == 6 and tx_list[i][:2].isalpha() and tx_list[i][2:].isnumeric():
                    val = tx_list[i]
                elif len(tx_list[i]) == 1 and (tx_list[i+1] == "Science" or tx_list[i+1] == "Professional" or tx_list[i+1] == "Engineering"):
                    key = tx_list[i]
                    flag = 1
            if flag == 1:
                tt[key] = val
                flag = 0

        df = pd.read_csv("Slotwise.csv")
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


        a= np.array(arr)

        with open('Timetable_'+user+'.csv', 'w', newline='') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(a)

        os.system("E:/Code/Python/Timetable_"+user+".csv")
    
        

app = QApplication(sys.argv)
w = Window()
sys.exit(app.exec_())
