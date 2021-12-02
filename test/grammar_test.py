import os
import psycopg2

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a seaotterhime').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE Words(
    ID serial PRIMARY KEY,
    Input VARCHAR (50) NOT NULL,
    Output VARCHAR (50) NOT NULL,
    Time VARCHAR (50) NOT NULL,
    Date VARCHAR (50) NOT NULL);''')
conn.commit()

cursor.close()
conn.close()