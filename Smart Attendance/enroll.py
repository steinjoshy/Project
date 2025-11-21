import os
from database import add_student

def enroll_student(name, student_id):
    try:
        import cv2
    except ImportError:
        print("Error: OpenCV (cv2) is not installed. Please install with 'pip install opencv-python'.")
        return False

    folder_path = f"dataset/{student_id}"
    os.makedirs(folder_path, exist_ok=True)

    # Check if student already exists
    from database import get_student
    if get_student(student_id):
        print(f"Student {student_id} already exists!")
        return False

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera. Please check that a webcam is connected and not used by another program.")
        return False

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0
    target_images = 15  # Capture 15 images
    
    print(f"Enrolling {name} ({student_id})")
    print("Instructions:")
    print("- Position your face in the center")
    print("- Press 'C' to capture (when face is detected)")
    print("- Press 'Q' to quit")
    
    while count < target_images:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw rectangle around detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Captured: {count}/{target_images}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("Enrollment - Press 'C' to capture, 'Q' to quit", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            if len(faces) > 0:
                # Crop face region
                x, y, w, h = faces[0]
                face_roi = frame[y:y+h, x:x+w]
                img_name = f"{folder_path}/{count}.jpg"
                cv2.imwrite(img_name, face_roi)
                count += 1
                print(f"Captured {count}/{target_images} images")
            else:
                print("No face detected! Please position your face properly.")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    if count >= 10:  # Minimum 10 images required
        add_student(name, student_id)
        print(f"Enrollment completed for {name} ({student_id})")
        return True
    else:
        print(f"Enrollment failed! Only {count} images captured. Need at least 10.")
        # Clean up incomplete enrollment
        import shutil
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        return False
