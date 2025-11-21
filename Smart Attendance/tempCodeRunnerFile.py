import tkinter as tk
from tkinter import messagebox
from enroll import enroll_student
from recognize import recognize_faces
from database import create_tables

create_tables()

def enroll_ui():
    name = name_entry.get()
    sid = id_entry.get()
    if name and sid:
        enroll_student(name, sid)
        messagebox.showinfo("Success", f"Enrollment completed for {name}")
    else:
        messagebox.showwarning("Error", "Please enter all details")

def recognize_ui():
    recognize_faces()
    messagebox.showinfo("Done", "Recognition completed")

root = tk.Tk()
root.title("Smart Attendance System")
root.geometry("400x300")
root.configure(bg="#cfe2f3")

tk.Label(root, text="Smart Attendance System", font=("Helvetica", 16, "bold"), bg="#cfe2f3").pack(pady=10)
tk.Label(root, text="Name:", bg="#cfe2f3").pack()
name_entry = tk.Entry(root)
name_entry.pack()
tk.Label(root, text="Student ID:", bg="#cfe2f3").pack()
id_entry = tk.Entry(root)
id_entry.pack()

tk.Button(root, text="Enroll Student", command=enroll_ui, bg="#6fa8dc", fg="white").pack(pady=10)
tk.Button(root, text="Mark Attendance", command=recognize_ui, bg="#3d85c6", fg="white").pack(pady=10)
tk.Button(root, text="Exit", command=root.destroy, bg="#0b5394", fg="white").pack(pady=10)

root.mainloop()
