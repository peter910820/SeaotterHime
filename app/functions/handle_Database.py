import os
import psycopg2
import datetime

from app.functions.handle_Time import *

def show_database():
    DATABASE_URL = os.environ['DATABASE_URL']
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()   
    print('DB Words is connect ok!')
    cursor.execute("SELECT Input, Output, Time, Date from Words")
    rows = cursor.fetchall()
    db0 = []
    db1 = []
    db2 = []
    db3 = []
    db4 = []
    db5 = []
    for row in rows:
        db0.append(row[0])
        db1.append(row[1])
        db2.append(row[2])
        db3.append(row[3])
    for column in range(len(db0)):
        db4 = [db0[column],db1[column],db2[column],db3[column]]
        db5.append(db4)
    return db5

def web_insert_database(Input,Output):
    DATABASE_URL = os.environ['DATABASE_URL']
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()   
    print('DB Words is connect ok!')
    timeDate = dateOperation()
    #insert database
    cursor.execute("INSERT INTO Words (Input, Output, Time, Date) VALUES (%s,%s,%s,%s)", (Input,Output,timeDate[0],timeDate[1]))
    database.commit()

def check_login(account, password):
    DATABASE_URL = os.environ['DATABASE_URL']
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()   
    print('DB UserDetailed is connect ok!')
    cursor.execute("SELECT Account, Password from UserDetailed")
    rows = cursor.fetchall()
    for i in range(len(rows)):
        if account == rows[i][0] and password == rows[i][1]:
            reminderMessage = "pass"
            return reminderMessage
        elif account == rows[i][0] and password != rows[i][1]:
            reminderMessage = "密碼輸入錯誤"
            return reminderMessage
        elif account == None or password == None:
            reminderMessage = "欄位不得為空"
            return reminderMessage
    return "查無此帳號"

def register_judge(account, password, passwordCheck, checkPwd):
    if  account == None or password == None or passwordCheck == None or checkPwd == None:
        return "欄位不得為空!"
    elif passwordCheck != password:
        return "密碼確認有誤!"
    elif checkPwd != "Arcaea":
        return "通行碼輸入錯誤!"
    else:
        DATABASE_URL = os.environ['DATABASE_URL']
        database = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = database.cursor()   
        print('DB UserDetailed is connect ok!')
        cursor.execute("SELECT Account, Password from UserDetailed")
        rows = cursor.fetchall()
        for i in range(len(rows)):
            if account == rows[i][0]:
               return "帳號已經存在!"  
        loc_dt = datetime.datetime.today() 
        time_del = datetime.timedelta(hours=8) 
        new_dt = loc_dt + time_del 
        datetime_format = new_dt.strftime("%Y/%m/%d %H:%M:%S")
        cursor.execute("INSERT INTO UserDetailed (Time, Account, Password) VALUES (%s,%s,%s)", (datetime_format,account,password))
        database.commit()
        cursor.close()
        database.close()
        return "帳號建立成功!"
def change_password_database(c_user, old_password, new_password, new_password_check):
    if old_password == None or new_password == None or new_password_check == None:
        return "欄位不得為空!"
    elif new_password != new_password_check:
        return "密碼確認有誤!"
    DATABASE_URL = os.environ['DATABASE_URL']
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()   
    print('DB UserDetailed is connect ok!')
    cursor.execute("SELECT Account, Password from UserDetailed")
    rows = cursor.fetchall()
    for i in range(len(rows)):
        if c_user == rows[i][0]:
            if old_password != rows[i][1]:
                return "原密碼輸入錯誤!"
            cursor.execute("UPDATE UserDetailed SET Password=(%s) WHERE account=(%s)",(new_password,c_user))
            database.commit()
            cursor.close()
            database.close()
            break
    return None