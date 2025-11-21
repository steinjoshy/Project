# Quick Start Guide

## First Time Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

## Step-by-Step Usage

### Step 1: Enroll Students
1. Open the application (`python app.py`)
2. Enter student name and ID
3. Click "Enroll Student"
4. Position face in front of webcam
5. Press 'C' to capture (capture 15 images)
6. Press 'Q' when done

### Step 2: Train Model
1. After enrolling students, click "Train Model"
2. Wait for embeddings to be generated
3. This improves recognition speed

### Step 3: Mark Attendance
1. Click "Mark Attendance"
2. Position face in front of webcam
3. System automatically recognizes and marks attendance
4. Press 'Q' to quit

### Step 4: View Attendance
1. Click "View Attendance"
2. Select date or view all
3. Browse attendance records

## Web Dashboard (Optional)

1. **Start Dashboard**
   ```bash
   python dashboard.py
   ```

2. **Access Dashboard**
   - Open browser: `http://localhost:5000`
   - Login: `admin` / `admin123`

3. **Features**
   - View statistics
   - Filter by date
   - Download CSV

## Troubleshooting

- **Webcam not working?** Check permissions and close other apps using webcam
- **Recognition slow?** Run "Train Model" to generate embeddings
- **Not recognizing?** Ensure good lighting and retrain model

## Tips

- Capture images in different lighting conditions during enrollment
- Train model after enrolling new students
- Use good lighting for better recognition accuracy
- Keep face centered in frame during recognition

