#CREATE A TO-DO LIST APP USING CRUDE
import sqlite3
con = sqlite3.connect("todolist.db")
cur = con.cursor() #manage database operation, fetch result, execute sql
con.execute (""" create table if not exists users(
             id integer primary key autoincrement,
             fullname varchar (30) not null,
             username varchar (30) unique not null,
             password varchar (30) not null
    )
""")

#todolist table for todolist details
con.execute(""" CREATE TABLE IF NOT EXISTS todos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task TEXT,
            status TEXT DEFAULT "pending"
            )
""")
con.commit()
con.close()