import os
import psycopg2

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a seaotterhime').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("SELECT ID, Time, Account, Password from UserDetailed")
rows = cursor.fetchall()
x = input("請輸入要刪除的帳號: ")
for i in range(len(rows)):
   if x == rows[i][2]:
      y = rows[i][0]
      cursor.execute("DELETE from UserDetailed where ID=(%s)",(y,))
      conn.commit()
print("Success!")
cursor.close()
conn.close()

cursor.close()
conn.close()