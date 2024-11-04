import pandas as pd
import sqlite3  as sqlite

conn =sqlite.connect("./database.db")

data=pd.read_csv("./recommender/data.csv")
data.to_sql("movie",conn,if_exists='replace',index=False)

cursor =conn.cursor()
for row in cursor.execute("select * from movie Limit 10"):
    print (row)
conn.close()
