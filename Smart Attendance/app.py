import tkinter as tk
from tkinter import messagebox, ttk
import datetime
from database import create_tables, get_today_attendance, get_all_attendance, get_attendance_by_date

create_tables()

def enroll_ui():
    name = name_entry.get().strip()
    sid = id_entry.get().strip()
    if name and sid:
        root.withdraw()  # Hide main window during enrollment
        try:
            from enroll import enroll_student
            success = enroll_student(name, sid)
        except ImportError as e:
            success = False
            messagebox.showerror("Dependency Error", "OpenCV is required for enrollment.\nInstall it with:\n\npip install opencv-python")
        root.deiconify()  # Show main window again
        if success:
            messagebox.showinfo("Success", f"Enrollment completed for {name}!\n\nPlease run 'Train Model' to generate embeddings.")
            name_entry.delete(0, tk.END)
            id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Enrollment failed or student already exists!")
    else:
        messagebox.showwarning("Error", "Please enter all details")

def recognize_ui():
    root.withdraw()
    try:
        from recognize import recognize_faces
        recognize_faces()
    except ImportError:
        messagebox.showerror("Dependency Error", "OpenCV is required for recognition.\nInstall it with:\n\npip install opencv-python")
    root.deiconify()
    messagebox.showinfo("Done", "Recognition session completed")

def train_model():
    result = messagebox.askyesno("Train Model", 
                                "This will generate embeddings for all enrolled students.\n"
                                "This may take a few minutes. Continue?")
    if result:
        root.withdraw()
        try:
            from train import generate_embeddings
            success = generate_embeddings()
            root.deiconify()
            if success:
                messagebox.showinfo("Success", "Model training completed successfully!")
            else:
                messagebox.showwarning("Warning", "Training completed with some issues.")
        except Exception as e:
            root.deiconify()
            messagebox.showerror("Error", f"Training failed: {str(e)}")

def view_attendance():
    attendance_window = tk.Toplevel(root)
    attendance_window.title("View Attendance")
    attendance_window.geometry("800x500")
    attendance_window.configure(bg="#f0f0f0")
    
    # Date selection
    date_frame = tk.Frame(attendance_window, bg="#f0f0f0")
    date_frame.pack(pady=10)
    
    tk.Label(date_frame, text="Select Date:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
    date_var = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
    date_entry = tk.Entry(date_frame, textvariable=date_var, width=12)
    date_entry.pack(side=tk.LEFT, padx=5)
    
    def load_attendance():
        date = date_var.get()
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            records = get_attendance_by_date(date)
        except:
            records = get_all_attendance()
        
        # Clear treeview
        for item in tree.get_children():
            tree.delete(item)
        
        if records:
            for record in records:
                # record format: (id, student_id, date, time, status, name)
                if len(record) >= 6:
                    tree.insert("", tk.END, values=(record[5], record[1], record[2], record[3], record[4]))
                else:
                    tree.insert("", tk.END, values=(record[1], record[2], record[3], record[4], record[5]))
        else:
            messagebox.showinfo("No Data", f"No attendance records found for {date}")
    
    tk.Button(date_frame, text="Load", command=load_attendance, bg="#6fa8dc", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(date_frame, text="View All", command=lambda: [date_var.set(""), load_attendance()], 
              bg="#3d85c6", fg="white").pack(side=tk.LEFT, padx=5)
    
    # Treeview for attendance table
    tree_frame = tk.Frame(attendance_window)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tree = ttk.Treeview(tree_frame, columns=("Name", "Student ID", "Date", "Time", "Status"), show="headings", height=15)
    tree.heading("Name", text="Name")
    tree.heading("Student ID", text="Student ID")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Status", text="Status")
    
    tree.column("Name", width=150)
    tree.column("Student ID", width=120)
    tree.column("Date", width=100)
    tree.column("Time", width=100)
    tree.column("Status", width=100)
    
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Load today's attendance by default
    load_attendance()

root = tk.Tk()
root.title("Smart Attendance System")
root.geometry("450x400")
root.configure(bg="#cfe2f3")

# Header
header = tk.Label(root, text="Smart Attendance System", font=("Helvetica", 18, "bold"), bg="#cfe2f3", fg="#0b5394")
header.pack(pady=15)

# Enrollment Section
enroll_frame = tk.LabelFrame(root, text="Enroll New Student", bg="#cfe2f3", font=("Helvetica", 10, "bold"))
enroll_frame.pack(pady=10, padx=20, fill=tk.X)

tk.Label(enroll_frame, text="Name:", bg="#cfe2f3").pack(anchor=tk.W, padx=10, pady=5)
name_entry = tk.Entry(enroll_frame, width=30)
name_entry.pack(padx=10, pady=5)

tk.Label(enroll_frame, text="Student ID:", bg="#cfe2f3").pack(anchor=tk.W, padx=10, pady=5)
id_entry = tk.Entry(enroll_frame, width=30)
id_entry.pack(padx=10, pady=5)

# Buttons
button_frame = tk.Frame(root, bg="#cfe2f3")
button_frame.pack(pady=15)

tk.Button(button_frame, text="Enroll Student", command=enroll_ui, bg="#6fa8dc", fg="white", 
          width=15, height=2, font=("Helvetica", 9, "bold")).pack(pady=5)

tk.Button(button_frame, text="Train Model", command=train_model, bg="#3d85c6", fg="white", 
          width=15, height=2, font=("Helvetica", 9, "bold")).pack(pady=5)

tk.Button(button_frame, text="Mark Attendance", command=recognize_ui, bg="#0b5394", fg="white", 
          width=15, height=2, font=("Helvetica", 9, "bold")).pack(pady=5)

tk.Button(button_frame, text="View Attendance", command=view_attendance, bg="#073763", fg="white", 
          width=15, height=2, font=("Helvetica", 9, "bold")).pack(pady=5)

tk.Button(button_frame, text="Exit", command=root.destroy, bg="#d32f2f", fg="white", 
          width=15, height=1, font=("Helvetica", 9)).pack(pady=10)

root.mainloop()
