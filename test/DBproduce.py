import os
import psycopg2
import datetime

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a seaotterhime').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

loc_dt = datetime.datetime.today()
loc_dt_format = loc_dt.strftime("%Y/%m/%d/%H:%M:%S")
a = "seaotterhime2"
p = "123456"
cursor.execute("INSERT INTO UserDetailed (Time, Account, Password) VALUES (%s,%s,%s)", (loc_dt_format,a,p))
conn.commit()
cursor.close()
conn.close()