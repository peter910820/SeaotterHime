import os
import psycopg2
import re

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a seaotterhime').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("SELECT Time, Account, Password from UserDetailed")
rows = cursor.fetchall()
db0 = []
db1 = []
db2 = []
db3 = []
for row in rows:
    db0.append(row[0])
    db1.append(row[1])
    db2.append(row[2])
for i in range(len(db1)):
    db3.append(f"{str(db0[i])} : {str(db1[i])} ----> {str(db2[i])}")
db3 = str(db3)
db3 = re.sub("\[|\'|\]","",db3)
print(db3.replace(', ',"\n"))

cursor.close()
conn.close()