import  customtkinter as ctk
from tkinter import messagebox as m
import speech_recognition as sr
import os
import sys

# ----------------- Resource Path -----------------

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ----------------- Task Functions -----------------


def add_task(event=0):
    task = entry.get()
    if task.strip() and task != "Enter a task...":
        task_label = ctk.CTkLabel(
            task_frame, text=task, font=("Segoe UI", 12), anchor="w"
        )
        task_label.pack(fill="x", pady=2, padx=10)
        task_label.bind("<Double-Button-1>", lambda e, lbl=task_label: edit_task(lbl))
        tasks.append(task_label)
        entry.delete(0, ctk.END)
    else:
        m.showwarning("Empty Input", "Please enter a task before adding.")


def edit_task(task_label):
    edit_win = ctk.CTkToplevel(app)
    edit_win.title("Edit Task")
    edit_win.geometry("300x100")
    edit_win.resizable(False, False)
    
    entry = ctk.CTkEntry(edit_win, width=250)
    entry.insert(0, task_label.cget("text"))
    entry.pack(pady=10)

    def save_edit():
        new_text = entry.get()
        if new_text.strip():
            task_label.configure(text=new_text)
            edit_win.destroy()
        else:
            m.showwarning("Empty Input", "Task cannot be empty.")

    save_btn = ctk.CTkButton(edit_win, text="Save", command=save_edit)
    save_btn.pack()

def delete_task():
    if tasks:
        tasks[-1].destroy()
        tasks.pop()
    else:
        m.showwarning("No Tasks", "No tasks to delete.")

def save_task():
    if tasks:
        with open("tasks.txt", "w") as f:
            for t in tasks:
                f.write(t.cget("text") + "\n")
        m.showinfo("Saved", "Tasks saved to tasks.txt")
    else:
        m.showwarning("No Tasks", "No tasks to save!")
        

def audio_recog(event=0):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        task = text
        if task.strip() and task != "Enter a task...":
            task_label = ctk.CTkLabel(
                task_frame, text=task, font=("Segoe UI", 12), anchor="w"
            )
            task_label.pack(fill="x", pady=2, padx=10)
            task_label.bind("<Double-Button-1>", lambda e, lbl=task_label: edit_task(lbl))
            tasks.append(task_label)
    except Exception as e:
        print("Error:", e)


def read_txt(event=0):
    # Clear old tasks
    for task in tasks:
        task.destroy()
    tasks.clear()

    try:
        with open("tasks.txt", "r") as f:
            task_lines = [line.strip() for line in f.readlines()]
        if not task_lines:
            task_lines = ["No tasks found."]
    except FileNotFoundError:
        task_lines = ["tasks.txt not found."]

    for task in task_lines:
        label = ctk.CTkLabel(task_frame, text=task, font=("Segoe UI", 12), anchor="w")
        label.pack(padx=10, pady=5, anchor="w")
        label.bind("<Double-Button-1>", lambda e, lbl=label: edit_task(lbl))
        tasks.append(label)



def clear_entry(event=0):
    entry.delete(0, ctk.END)


def show_about():
    m.showinfo("About", "Modern ToDo App\nBy Manish")


# ----------------- GUI Setup -----------------
    
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("Modern ToDo App")
app.geometry("400x500")
app.resizable(False, False)


#-------------- Store CTkLabel widgets -------------

tasks = []

# ----------------- Top Button Bar -----------------

top_bar = ctk.CTkFrame(app, fg_color="transparent")
top_bar.pack(fill="x", padx=10, pady=10)

bottom_bar = ctk.CTkFrame(app, fg_color="transparent")
bottom_bar.pack(fill="x", side="bottom", padx=10, pady=10)

save_btn = ctk.CTkButton(top_bar, text="Save", width=80, command=save_task, fg_color="#059862")
save_btn.pack(side="left")

about_btn = ctk.CTkButton(top_bar, text="About", width=80, command=show_about)
about_btn.pack(side="right")

speech_btn = ctk.CTkButton(top_bar, text="Speak", width=80, command=audio_recog)
speech_btn.pack(side="right", padx=69)

exit_btn = ctk.CTkButton(bottom_bar, text="Exit", width=80, command=app.quit, fg_color="#E43A37")
exit_btn.pack(side="right")

open_btn = ctk.CTkButton(bottom_bar, text="Open", width=80, command=read_txt)
open_btn.pack(side="left")

# ----------------- Entry Field -------------------

entry = ctk.CTkEntry(app, placeholder_text="Enter a task...", width=280, height=40, font=("Segoe UI", 12))
entry.pack(padx=20, pady=(0, 10))

entry.bind("<Return>", add_task)
entry.bind("<Delete>", clear_entry)

# ----------------- Action Buttons -----------------

action_frame = ctk.CTkFrame(app, fg_color="transparent")
action_frame.pack(pady=5)

add_btn = ctk.CTkButton(action_frame, text="Add", width=100, command=add_task)
add_btn.pack(side="left", padx=10)

del_btn = ctk.CTkButton(action_frame, text="Delete", width=100, command=delete_task)
del_btn.pack(side="right", padx=10)

# ----------------- Task Display -----------------

scroll_container = ctk.CTkScrollableFrame(app, width=360, height=300)
scroll_container.pack(padx=20, pady=10, fill="both", expand=False)

#--------------- where task labels go ----------------

task_frame = scroll_container

# ----------------- Mainloop -----------------

app.mainloop()