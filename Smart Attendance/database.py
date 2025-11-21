import sqlite3
import datetime

def create_tables():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    student_id TEXT UNIQUE NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Present',
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                )''')
    conn.commit()
    conn.close()

def add_student(name, student_id):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO students (name, student_id) VALUES (?, ?)", (name, student_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_student(student_id):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    result = c.fetchone()
    conn.close()
    return result

def get_all_students():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    results = c.fetchall()
    conn.close()
    return results

def mark_attendance(student_id, date, time, status="Present"):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    # Check if already marked today
    c.execute("SELECT * FROM attendance WHERE student_id = ? AND date = ?", (student_id, date))
    if c.fetchone():
        conn.close()
        return False  # Already marked
    c.execute("INSERT INTO attendance (student_id, date, time, status) VALUES (?, ?, ?, ?)",
              (student_id, date, time, status))
    conn.commit()
    conn.close()
    return True

def get_attendance_by_date(date):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT a.*, s.name 
                 FROM attendance a 
                 JOIN students s ON a.student_id = s.student_id 
                 WHERE a.date = ? 
                 ORDER BY a.time''', (date,))
    results = c.fetchall()
    conn.close()
    return results

def get_attendance_by_student(student_id):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM attendance 
                 WHERE student_id = ? 
                 ORDER BY date DESC, time DESC''', (student_id,))
    results = c.fetchall()
    conn.close()
    return results

def get_all_attendance():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT a.*, s.name 
                 FROM attendance a 
                 JOIN students s ON a.student_id = s.student_id 
                 ORDER BY a.date DESC, a.time DESC''')
    results = c.fetchall()
    conn.close()
    return results

def get_today_attendance():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return get_attendance_by_date(today)
