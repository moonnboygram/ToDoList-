import tkinter as tk
import sqlite3
from tkinter import messagebox as msg

#get your user id from login
user_id = "123"
    

master = tk.Tk()
master.title("Todo Dashboard")
master.geometry("500x500+0+0")
master.config (background= "black")

 
def refreshtask():
    listbox.delete(0, tk.END)
    con = sqlite3.connect("todolist.db")
    cur = con.cursor()
    


    cur.execute (""" select id, task, status from todos where user_id = ?
                 """, (user_id,))
    rows = cur.fetchall()
    

    for row in rows:
        status_icon = "✅" if row[2] == "done" else "⏳"
        listbox.insert(tk.END, f"{row[0]} | {row[1]} | {status_icon}")

    con.close()

# -------- CREATE --------
def add_task():
    task_text = entry.get()
    
        # var = tk.IntVar()
        # checkbtn = tk.Checkbutton (master, text = add_task, variable = var)
        # checkbtn.pack (anchor = "w")
    if not task_text:
        msg.showinfo ("Alert", "Enter a task")

        return

    con = sqlite3.connect("todolist.db")
    cur = con.cursor()

    cur.execute (""" insert into todos (user_id, task, status)
                 values(?,?, "pending") """, (user_id, task_text))
    
    con.commit()
    con.close()

    entry.delete(0, tk.END)
    refreshtask()

    # -------- DELETE --------

def delete_task():
    selected = listbox.get(tk.ACTIVE)
    if selected == "":
        msg.showinfo("propt", "Empty fields")
        return
    confirm = msg.askyesno ("Confirm", "Would you like to delete this task?")
    
    if not confirm:
        return
    # if not listbox.curselection():
    #     confirm = msg.askyesno ("Confirm", "Would you like to delete this task?")
    #     return
    # selected = listbox.get(listbox.curselection ())

    task_id = selected.split("|")[0].strip()

    con = sqlite3.connect("todolist.db")
    cur = con.cursor()

    cur.execute (""" DELETE FROM todos WHERE id = ? """, (task_id,))
    con.commit()
    con.close()

    refreshtask()

# -------- UPDATE --------

def mark_done():
    if not listbox.curselection():
        msg.showinfo("Alert", "select a task first")
        return
    selected = listbox.get(listbox.curselection()[0])
    task_id = selected.split ("|")[0].strip()
    
    con = sqlite3.connect("todolist.db")
    cur = con.cursor()
    
    cur.execute (""" UPDATE todos SET status = "done" 
                 WHERE id = ? """, (task_id,))
    
    con.commit()
    con.close()

    refreshtask()



# -------- UI --------
entry = tk.Entry (master, width = 40)
entry.pack(pady = 10)

add_btn = tk.Button (master, text = 'Add Task', font = ("Arial",10), fg = "white", bg = "red"
                     , command = add_task)
add_btn.pack()

listbox = tk.Listbox (master, height= 15, width = 50)
listbox.pack (pady = 10)


donebtn = tk.Button (master, text = "Done", font = ("Arial", 10), fg = "white", bg = "red",
                     command = mark_done)
donebtn.pack()

deletebtn = tk.Button (master, text = "Delete", font = ("Arial", 10), fg = "white", bg = "red",
                    command = delete_task)
deletebtn.place(x =100, y = 330)


refreshbtn = tk.Button (master, text = "Refresh", font = ("Arial", 10),fg = "white", bg = "red",
                        command = refreshtask)
refreshbtn.place (x = 346, y = 330)

refreshtask()

master.mainloop()