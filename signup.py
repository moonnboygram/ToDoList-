#CREATE A TO-DO LIST APP USING CRUDE
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from tkinter import messagebox as message
import sqlite3
import hashlib

master = tk.Tk()
master.geometry("700x500+300+0")
master.title("MY TO-DO LIST")
master.configure(background=  "pink")
# image =Image.open ("bg.jpg")
# photo = ImageTk.PhotoImage(image)



def signup():
    subprocess.Popen (["python", "signin.py"]) #subprocess.Popen opens another page

def sign():
    fullname = entry1.get()
    username = entry2.get()
    password = entry3.get()

    if fullname == "" or username == "" or password == "":
        message.showinfo ("Alert", "Empty record noy allowed")
        return
    
    try:
        con = sqlite3.connect("todolist.db")
        cur = con.cursor()

        hashed_password = hashlib.sha256 (password.encode()).hexdigest()
        cur.execute ("""insert into users(fullname, username, password)
                     values(?,?,?)""",(fullname, username, hashed_password))

        con.commit()
        con.close()

        message.showinfo("Alert", "Sign up successful")
        master.destroy()
        signup()

    except sqlite3.IntegrityError:
        message.showinfo ("Alert", "Username already exist")



        
dashboard = tk.Label (master, text = "Sign up MY TO-DO LIST", font = ("verdana", 20,"bold"),bg = "pink", fg = "black")
dashboard.place (x = 160, y = 10)

fullname = tk.Label (master, text = "Fullname:", font = ("verdana", 10, "bold"), bg = "pink", fg = "black")
fullname.place (x = 10, y = 80)
entry1 = tk.Entry (master, width = 50, bg = "pink")
entry1.place (x = 100, y = 82)

username = tk.Label (master, text = "Username:", font = ("verdana", 10,"bold"), bg = "pink", fg = "black")
username.place (x =10 , y = 120)
entry2 = tk.Entry (master, width = 50, bg = "pink")
entry2.place (x = 100, y = 120)

password = tk.Label (master, text = "Password:", font = ("verdana",10, "bold"), bg = "pink", fg = "black")
password.place (x = 10, y = 160)
entry3 = tk.Entry (master, width = 50, bg = "pink", show = "*")
entry3.place (x = 100, y = 160)

btn = tk.Button (master, text = "SIGN UP", font = ("verdana", 10, "bold"), bg = "pink", fg = "black", width = 10, command = sign)
btn.place (x = 190, y = 200)
password = tk.Label ()
# add_button = tk.Button (master, text = "Add Task", font = ("verdana", 10, "bold"), bg = "pink", fg = "black")
# add_button. place (x = 280, y =100)



master.mainloop()
