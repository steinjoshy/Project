from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
import csv
import io
import datetime
from database import get_all_attendance, get_attendance_by_date, get_today_attendance, get_all_students
from functools import wraps

app = Flask(__name__)
app.secret_key = 'smart_attendance_secret_key_2024'  # Change this in production

# Simple authentication (replace with proper auth in production)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'  # Change this!

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_attendance = get_today_attendance()
    total_students = len(get_all_students())
    present_today = len(today_attendance)
    
    stats = {
        'total_students': total_students,
        'present_today': present_today,
        'absent_today': total_students - present_today,
        'today_date': today
    }
    
    return render_template('dashboard.html', stats=stats, attendance=today_attendance)

@app.route('/attendance')
@login_required
def attendance():
    date = request.args.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))
    
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        records = get_attendance_by_date(date)
    except:
        records = get_all_attendance()
        date = "All"
    
    return render_template('attendance.html', attendance=records, selected_date=date)

@app.route('/download')
@login_required
def download():
    date = request.args.get('date', '')
    
    if date:
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            records = get_attendance_by_date(date)
            filename = f'attendance_{date}.csv'
        except:
            records = get_all_attendance()
            filename = 'attendance_all.csv'
    else:
        records = get_all_attendance()
        filename = 'attendance_all.csv'
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Student ID', 'Name', 'Date', 'Time', 'Status'])
    
    # Write data
    for record in records:
        if len(record) >= 6:
            # Format: (id, student_id, date, time, status, name)
            writer.writerow([record[0], record[1], record[5], record[2], record[3], record[4]])
        else:
            writer.writerow(record)
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/stats')
@login_required
def api_stats():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_attendance = get_today_attendance()
    total_students = len(get_all_students())
    present_today = len(today_attendance)
    
    return jsonify({
        'total_students': total_students,
        'present_today': present_today,
        'absent_today': total_students - present_today,
        'today_date': today
    })

if __name__ == '__main__':
    print("Starting Flask Dashboard...")
    print("Access the dashboard at: http://localhost:5000")
    print("Default credentials: admin / admin123")
    app.run(debug=True, host='0.0.0.0', port=5000)

