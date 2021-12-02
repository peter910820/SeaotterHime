import os
import psycopg2
import re

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a seaotterhime').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("SELECT Input, Output, Time, Date from Words")
rows = cursor.fetchall()
db0 = []
db1 = []
db2 = []
db3 = []
db4 = []
for row in rows:
    db0.append(row[0])
    db1.append(row[1])
    db2.append(row[2])
    db4.append(row[3])
for i in range(len(db1)):
    db3.append(f"{str(db0[i])} ----> {str(db1[i])} {str(db2[i])} {str(db4[i])}")
db3 = str(db3)
print(db3)

cursor.close()
conn.close()