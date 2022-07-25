import webbrowser
import time
import pyautogui as pg
import pwinput
from nltk.tokenize import word_tokenize
import re
import pandas as pd
import numpy as np
import csv
import os
import subprocess


def clrscr():
    clear = lambda: os.system("cls")
    clear()


def creds():
    username = str(input("Username : "))
    password = pwinput.pwinput(prompt="Password : ")
    return username, password


def workflow():
    url = "https://workflow.iitm.ac.in/"
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser("C:/Program Files/Mozilla Firefox/firefox.exe"))
    webbrowser.get('firefox').open(url)


def access(username, password):
    width, height = pg.size()
    time.sleep(3)
    pg.click(width/2, height/4)
    pg.write(username)
    time.sleep(1)
    pg.click(width/2, height/2.9)
    pg.write(password)
    time.sleep(1)
    pg.click(width/1.8, height/2.4)


def portal(username, password):
    width, height = pg.size()
    time.sleep(2)
    pg.click(width/3.5, height/1.78)
    time.sleep(3)
    pg.click(width/2, height/2.3)
    pg.write(username)
    time.sleep(1)
    pg.click(width/2, height/1.76)
    pg.write(password)
    pg.click(width/1.8, height/1.5)


def copy():
    time.sleep(4)
    w, h = pg.size()

    pg.moveTo(w/3.6, h/1.8)
    pg.dragTo(w/1.35, h/1.1, 1, button='left')
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
user, pwd = creds()
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
