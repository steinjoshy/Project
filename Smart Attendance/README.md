# Smart Attendance System using Face Recognition

A comprehensive attendance management system that automates attendance marking using face recognition technology. Built with Python, DeepFace, Tkinter, SQLite, and Flask.

## 🎯 Features

- **Student Enrollment**: Capture and store student face images via webcam
- **Face Recognition**: Real-time face detection and recognition for automatic attendance marking
- **Embedding Generation**: Pre-computed embeddings for faster recognition
- **Attendance Management**: SQLite database for storing attendance records
- **Tkinter GUI**: User-friendly desktop interface for enrollment and attendance
- **Flask Dashboard**: Web-based admin dashboard with login, attendance viewing, and CSV export
- **Duplicate Prevention**: Prevents multiple attendance entries for the same student on the same day

## 📋 System Requirements

### Hardware
- Laptop/PC with webcam
- ≥4 GB RAM (8 GB recommended)
- i3 / Ryzen 3 or above
- (Optional) NVIDIA GPU for faster recognition

### Software
- OS: Windows/Linux/Mac
- Python: 3.8–3.11
- Webcam access

## 🚀 Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Note: `sqlite3` and `tkinter` are pre-installed with Python on most systems.

3. **Verify installation:**
   ```bash
   python -c "import cv2, deepface, flask; print('All dependencies installed!')"
   ```

## 📁 Project Structure

```
SmartAttendance/
│── dataset/          # Student face images (auto-created)
│── models/           # Stored embeddings (auto-created)
│── templates/        # Flask HTML templates
│── attendance.db     # SQLite database (auto-created)
│── app.py            # Main Tkinter GUI application
│── enroll.py         # Student enrollment module
│── recognize.py      # Face recognition module
│── train.py          # Embedding generation module
│── database.py       # Database operations
│── dashboard.py      # Flask web dashboard
│── requirements.txt  # Python dependencies
│── README.md         # This file
```

## 🎮 Usage

### 1. Start the Main Application

Run the Tkinter GUI:
```bash
python app.py
```

### 2. Enroll Students

1. Enter student name and ID in the GUI
2. Click "Enroll Student"
3. Position face in front of webcam
4. Press 'C' to capture images (capture 15 images)
5. Press 'Q' to finish enrollment

### 3. Train the Model

After enrolling students, generate embeddings:
1. Click "Train Model" in the GUI
2. Wait for embeddings to be generated (may take a few minutes)
3. This improves recognition speed significantly

### 4. Mark Attendance

1. Click "Mark Attendance" in the GUI
2. Position face in front of webcam
3. System will automatically detect and recognize faces
4. Attendance is marked in the database
5. Press 'Q' to quit recognition

### 5. View Attendance

1. Click "View Attendance" in the GUI
2. Select a date or view all records
3. Attendance table displays all records

### 6. Flask Dashboard (Optional)

Start the web dashboard:
```bash
python dashboard.py
```

Access at: `http://localhost:5000`

**Default Login:**
- Username: `admin`
- Password: `admin123`

**Features:**
- View today's attendance statistics
- Filter attendance by date
- Download attendance as CSV
- View all attendance records

## 🔧 Module Details

### Enrollment Module (`enroll.py`)
- Captures 15 face images per student
- Uses Haar Cascade for face detection
- Stores images in `dataset/<student_id>/`
- Adds student record to database

### Training Module (`train.py`)
- Generates face embeddings using DeepFace
- Stores embeddings in `models/embeddings.pkl`
- Significantly improves recognition speed

### Recognition Module (`recognize.py`)
- Real-time face detection and recognition
- Uses pre-generated embeddings for fast matching
- Prevents duplicate attendance entries
- Cooldown period between recognitions

### Database Module (`database.py`)
- SQLite database operations
- Tables: `students`, `attendance`
- Functions for CRUD operations

## 📊 Database Schema

### Students Table
- `id`: Primary key
- `name`: Student name
- `student_id`: Unique student identifier

### Attendance Table
- `id`: Primary key
- `student_id`: Foreign key to students
- `date`: Attendance date (YYYY-MM-DD)
- `time`: Attendance time (HH:MM:SS)
- `status`: Attendance status (default: "Present")

## 🎨 Features in Detail

### Face Detection
- Uses OpenCV Haar Cascade for real-time face detection
- Visual feedback with bounding boxes

### Face Recognition
- DeepFace library with Facenet model
- Cosine distance for matching
- Configurable recognition threshold

### Duplicate Prevention
- Checks if attendance already marked for the day
- Cooldown period to prevent rapid re-recognition

### Performance Optimization
- Processes every 5th frame for better performance
- Pre-generated embeddings for faster lookup
- Efficient database queries

## 🔒 Security Notes

- Change default admin credentials in `dashboard.py` for production
- Update Flask secret key in `dashboard.py`
- Consider adding proper authentication for production use

## 🐛 Troubleshooting

### Webcam not working
- Check webcam permissions
- Ensure no other application is using the webcam
- Try changing camera index in `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`

### Recognition not accurate
- Ensure good lighting conditions
- Capture more training images (15+ recommended)
- Retrain the model after adding new students
- Adjust recognition threshold in `recognize.py`

### DeepFace installation issues
- Ensure TensorFlow is properly installed
- Try: `pip install --upgrade tensorflow deepface`

### Database errors
- Delete `attendance.db` to reset database
- Ensure write permissions in project directory

## 📈 Future Enhancements

- Email notifications for daily attendance summary
- Mask detection and handling
- Multi-face detection in single frame
- Attendance reports and analytics
- Mobile app integration
- Cloud database support

## 📝 License

This project is created for educational purposes.

## 👥 Credits

Built as part of a Mini Project using:
- DeepFace for face recognition
- OpenCV for computer vision
- Tkinter for GUI
- Flask for web dashboard
- SQLite for database

## 📞 Support

For issues or questions, please check:
1. All dependencies are installed correctly
2. Webcam is working and accessible
3. Database file has proper permissions
4. Python version is 3.8-3.11

---

**Note**: This system is designed for educational purposes. For production use, consider additional security measures and proper authentication systems.

