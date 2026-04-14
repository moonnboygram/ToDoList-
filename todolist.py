import tkinter as tk
import sqlite3
from tkinter import messagebox as msg

user_id = "123"

master = tk.Tk()
master.title("Todo Dashboard")
master.geometry("500x500+0+0")
master.config(background="black")

# ---------------- REFRESH ----------------
def refreshtask():
    listbox.delete(0, tk.END)

    con = sqlite3.connect("todolist.db")
    cur = con.cursor()

    cur.execute("SELECT id, task, status FROM todos WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()

    for row in rows:
        status_icon = "✅" if row[2] == "done" else "⏳"
        listbox.insert(tk.END, f"{row[0]} | {row[1]} | {status_icon}")

    con.close()

# ---------------- SELECT TASK ----------------
def on_select(event):
    if not listbox.curselection():
        return

    selected = listbox.get(listbox.curselection()[0])
    parts = selected.split(" | ")

    entry.delete(0, tk.END)
    entry.insert(0, parts[1])

# ---------------- UPDATE ----------------
def updatetask():
    if not listbox.curselection():
        msg.showinfo("Alert", "Select a task first")
        return

    task_text = entry.get()
    if not task_text:
        msg.showinfo("Alert", "Enter new task text")
        return

    selected = listbox.get(listbox.curselection()[0])
    task_id = selected.split(" | ")[0].strip()

    con = sqlite3.connect("todolist.db")
    cur = con.cursor()

    cur.execute("UPDATE todos SET task = ? WHERE id = ?", (task_text, task_id))

    con.commit()
    con.close()

    entry.delete(0, tk.END)
    refreshtask()

# ---------------- ADD ----------------
def add_task():
    task_text = entry.get()

    if not task_text:
        msg.showinfo("Alert", "Enter a task")
        return

    con = sqlite3.connect("todolist.db")
    cur = con.cursor()

    cur.execute(
        "INSERT INTO todos (user_id, task, status) VALUES (?, ?, 'pending')",
        (user_id, task_text)
    )

    con.commit()
    con.close()

    entry.delete(0, tk.END)
    refreshtask()

# ---------------- DELETE ----------------
def delete_task():
    if not listbox.curselection():
        msg.showinfo("Prompt", "Select a task first")
        return

    selected = listbox.get(listbox.curselection()[0])
    task_id = selected.split(" | ")[0].strip()

    con = sqlite3.connect("todolist.db")
    cur = con.cursor()
    
    # delete selected task
    cur.execute("DELETE FROM todos WHERE id = ?", (task_id,))
    
    #check if table is empty
    cur.execute("SELECT COUNT(*) FROM todos WHERE user_id = ?", (user_id,))
    count = cur.fetchone()[0]

    # reset auto-increment if empty
    if count == 0:
        cur.execute("DELETE FROM sqlite_sequence WHERE name = 'todos'")

    con.commit()
    con.close()

    refreshtask()

# ---------------- DONE ----------------
def mark_done():
    if not listbox.curselection():
        msg.showinfo("Alert", "Select a task first")
        return

    selected = listbox.get(listbox.curselection()[0])
    task_id = selected.split(" | ")[0].strip()

    con = sqlite3.connect("todolist.db")
    cur = con.cursor()

    cur.execute("UPDATE todos SET status = 'done' WHERE id = ?", (task_id,))

    con.commit()
    con.close()

    refreshtask()

# ---------------- UI ----------------
entry = tk.Entry(master, width=40)
entry.pack(pady=10)

add_btn = tk.Button(master, text="Add Task", fg="white", bg="black", command=add_task)
add_btn.pack()

listbox = tk.Listbox(master, height=15, width=50)
listbox.pack(pady=10)

listbox.bind("<<ListboxSelect>>", on_select)

donebtn = tk.Button(master, text="Done", fg="white", bg="black", command=mark_done)
donebtn.pack()

deletebtn = tk.Button(master, text="Delete", fg="white", bg="black", command=delete_task)
deletebtn.place(x=100, y=330)

updatebtn = tk.Button(master, text="Update", fg="white", bg="black", command=updatetask)
updatebtn.place(x=352, y=330)

# ---------------- START ----------------
refreshtask()
master.mainloop()