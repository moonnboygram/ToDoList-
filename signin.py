import tkinter as tk
master = tk.Tk()
import subprocess
from tkinter import messagebox as msg
import sqlite3
import hashlib
master.geometry("700x500+300+0")
master.title("login todolist")
master.configure(background = "black")


def todolist():
    subprocess.Popen (["python", "todolist.py"])


def login():
    username = entry1.get()
    password = entry2.get()
    
    if username =="" or password == "":
        msg.showinfo("Alert", "Enter your username and password")

        
    
        # msg.showinfo("prompt", "Username or password is incorrect")
    
        return
    
    con = sqlite3.connect ("todolist.db")
    cur = con.cursor()
    hashed_password = hashlib.sha256 (password.encode()).hexdigest()

    cur.execute(""" select * from users where username = ? and password = ? """, (username, hashed_password))
    result = cur.fetchone()

    if result:
        user_id = result[0]

        msg.showinfo("Alert", "Login successful")
        con.close()
        master.destroy()

        subprocess.Popen(["python", "todolist.py", str(user_id)])
    else:
        msg.showinfo("Alert", "Invalid username or password")
        con.close()
        




dashboard = tk.Label (master, text = "signin", font = ("verdana", 20), bg = "black", fg = "white")
dashboard.place (x = 280, y = 10)

username = tk.Label (master, text = "Username", font = ("verdana", 10), bg = "black", fg = "white") 
username.place (x = 10, y = 200)
entry1 = tk.Entry (master, width = 50, bg = "white")
entry1.place (x = 180, y = 202)

password = tk.Label(master, text = "password", font = ("verdana", 10), bg = "black", fg = "white")
password.place (x = 10, y = 250)
entry2 = tk.Entry (master, width = 50, bg = "white", show = "*")
entry2.place (x = 180, y = 251)

login = tk.Button (master, text = "Login", font = ("verdana", 10), bg = "black", fg = "white",
                   width = 5, command = login)
login.place (x = 330, y = 330)

master.mainloop()