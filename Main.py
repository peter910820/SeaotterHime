import uvicorn
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

import os
import re
import psycopg2
import datetime

from app.testMessage_def import test_Word
from app.hentai_def import nhentai_Search
from app.randomChoice_def import *
from app.arcaeaGroup_def import *
from app.spider_def import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# LineBot客戶端 #
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN']) #heroku set config vars
handler = WebhookHandler(os.environ['CHANNEL_SECRET']) #heroku set config vars

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    body = body.decode('utf-8', 'replace')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        HTTPException(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    DATABASE_URL = os.environ['DATABASE_URL']
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()
    print('Database is Connect ok!')
    msg = event.message.text
    msg = msg.encode('utf-8')
    msg = []
    cursor.execute("SELECT Input, Output from Words")
    rows = cursor.fetchall()
    for i in range(len(rows)):
        if event.message.text == rows[i][0]:
            msg.append(TextSendMessage(text = rows[i][1]))
    if event.message.text == '$test':
        msg.append(TextSendMessage(text = test_Word()))
    
# /command:
    # /search
    if event.message.text == '/search':
        cursor.execute("SELECT Input, Output from Words")
        rows = cursor.fetchall()
        db1 = []
        db2 = []
        db3 = []
        for row in rows:
            db1.append(row[0])
            db2.append(row[1])
        for i in range(len(db1)):
            db3.append(f"{str(db1[i])} ---> {str(db2[i])}")
        db3 = str(db3)
        db3 = re.sub("\[|\'|\]","",db3)
        msg.append(TextSendMessage(text = db3.replace(', ',"\n")))
    # /insert
    if re.match(r'^[/][I][N][S][E][R][T][-][a-zA-Z0-9_/:.\u4e00-\u9fa5]{1,20}[-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,40}$', event.message.text):
        messageList = event.message.text
        messageList = messageList.split('-')
        messageIN = messageList[1]
        messageOUT = messageList[2]
        loc_dt = datetime.datetime.today() 
        time_del = datetime.timedelta(hours=8) 
        new_dt = loc_dt + time_del 
        time_format = new_dt.strftime("%H:%M:%S")
        date_format = new_dt.strftime("%Y/%m/%d")
        #insert database
        cursor.execute("INSERT INTO Words (Input, Output, Time, Date) VALUES (%s,%s,%s,%s)", (messageIN,messageOUT,time_format,date_format))
        database.commit()
        msg.append(TextSendMessage(text=f'輸入出組合: {messageIN}-{messageOUT} 已成功設置'))
    # /delete
    if re.match(r'^[/][D][E][L][-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,20}$', event.message.text):
        messageList = event.message.text
        messageList = messageList.split('-')
        messageDEL = messageList[1]
        cursor.execute("SELECT ID, Input, Output, Time, Date from Words")
        rows = cursor.fetchall()
        for i in range(len(rows)):
            if messageDEL == rows[i][1]:
                y = rows[i][0]
                cursor.execute("DELETE from Words where ID=(%s)",(y,))
                database.commit()
        msg.append(TextSendMessage(text=f'{messageDEL} 已成功刪除'))
    #Google功能
    if re.match(r'^[$][g][o][o][g][l][e][-][a-zA-Z0-9__/:.\u4e00-\u9fa5]{1,20}$', event.message.text):
        msg.append(TextSendMessage(text = google_Search(event.message.text)))
#arcaea群組會用到的功能(((===============================================================
    if "dc" in event.message.text or "DC" in event.message.text or "Dc" in event.message.text:
        msg.append(TextSendMessage(text = dc_Publicity()))
    if "查" in  event.message.text:
        msg.append(TextSendMessage(text = score_Search()))
    if "群規" in event.message.text:
        msg.append(TextSendMessage(text = arcaea_Roles()))
    if "vc" in event.message.text or "VC" in event.message.text or "Vc" in event.message.text:
        msg.append(TextSendMessage(text = snowth("VC")))
    if "天堂門" in event.message.text:
        msg.append(TextSendMessage(text = snowth("天堂門")))
#arcaea群組會用到的功能(((===============================================================
#群組會用到的功能(((=====================================================================
    if "運勢" in event.message.text:
        msg.append(TextSendMessage(text = fortunate()))
    if re.match(r'^[N][0-9]{1,6}$', event.message.text) or re.match(r'^[n][0-9]{1,6}$', event.message.text):
        msg.append(TextSendMessage(text = nhentai_Search(event.message.text)))
#群組會用到的功能(((=====================================================================
    line_bot_api.reply_message(event.reply_token, messages=msg[:5])
    cursor.close()   #關閉游標
    database.close() #關閉DB


# 網頁端 #
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("homePage.html", {"request": request})
@app.get("/introduce", response_class=HTMLResponse) 
async def read_item(request: Request):
    return templates.TemplateResponse("introduce.html", {"request": request})
    
@app.post("/insert_Complete", response_class=HTMLResponse) 
async def read_item(request: Request, Input:str=Form(None), Output:str=Form(None)):
    DATABASE_URL = os.environ['DATABASE_URL']
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()   
    print('Database is Connect ok!')
    loc_dt = datetime.datetime.today() 
    time_del = datetime.timedelta(hours=8) 
    new_dt = loc_dt + time_del 
    time_format = new_dt.strftime("%H:%M:%S")
    date_format = new_dt.strftime("%Y/%m/%d")
    #insert database
    cursor.execute("INSERT INTO Words (Input, Output, Time, Date) VALUES (%s,%s,%s,%s)", (Input,Output,time_format,date_format))
    database.commit()
    return templates.TemplateResponse("insert_Complete.html", {"request": request})

@app.get("/database", response_class=HTMLResponse) 
async def read_item(request: Request):
    DATABASE_URL = os.environ['DATABASE_URL']
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()   
    print('Database is Connect ok!')
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
    return templates.TemplateResponse("database.html", {"request": request, "data" : db5})
#註冊#
@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
#註冊狀態#
@app.post("/register/judge")
async def register_judge(request: Request, account:str=Form(None), 
                        password:str=Form(None), passwordCheck:str=Form(None),checkPwd:str=Form(None)):
    if checkPwd != "Arcaea" or passwordCheck != password or account == None or password == None or passwordCheck == None or checkPwd == None:
        return templates.TemplateResponse("register_Fail.html", {"request": request})
    else:
        DATABASE_URL = os.environ['DATABASE_URL']
        database = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = database.cursor()   
        print('Database is Connect ok!')
        cursor.execute("SELECT Account, Password from UserDetailed")
        rows = cursor.fetchall()
        for i in range(len(rows)):
            if account == rows[i][0]:
               return templates.TemplateResponse("register_Fail.html", {"request": request})  
        loc_dt = datetime.datetime.today() 
        time_del = datetime.timedelta(hours=8) 
        new_dt = loc_dt + time_del 
        datetime_format = new_dt.strftime("%Y/%m/%d %H:%M:%S")
        cursor.execute("INSERT INTO UserDetailed (Time, Account, Password) VALUES (%s,%s,%s)", (datetime_format,account,password))
        database.commit()
        cursor.close()
        database.close()
        return templates.TemplateResponse("register_Success.html", {"request": request})
#登入#
@app.post('/submit')
async def get_user(request:Request, account:str=Form(None), password:str=Form(None)):
    DATABASE_URL = os.environ['DATABASE_URL']
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()   
    print('Database is Connect ok!')
    cursor.execute("SELECT Account, Password from UserDetailed")
    rows = cursor.fetchall()
    for i in range(len(rows)):
        if account == rows[i][0] and password == rows[i][1]:
            return templates.TemplateResponse('home.html',{'request':request,'account':account})
        elif  account == None or password == None:
            reminderMessage = "欄位不得為空"
            return templates.TemplateResponse('submit_Fail.html',{'request':request, 'reminderMessage':reminderMessage})
    reminderMessage = "查無此帳號"
    return templates.TemplateResponse('submit_Fail.html',{'request':request, 'reminderMessage':reminderMessage})

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("Main:app", host="0.0.0.0", port=port, reload=True)