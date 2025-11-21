import os
import datetime
import numpy as np
from database import mark_attendance, get_student
from train import load_embeddings

THRESHOLD = float(os.getenv("ATTENDANCE_THRESHOLD", "0.35"))

def _require_opencv():
    try:
        import cv2  # type: ignore
        return cv2
    except ImportError:
        print("Error: OpenCV (cv2) is not installed. Install with 'pip install opencv-python'.")
        return None

def _require_deepface():
    try:
        from deepface import DeepFace  # type: ignore
        return DeepFace
    except ImportError:
        print("Error: The 'deepface' package is not installed. Install with 'pip install deepface'.")
        return None

def _cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Return cosine distance between two vectors."""
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if a_norm == 0 or b_norm == 0:
        return float("inf")
    return 1.0 - float(np.dot(a, b) / (a_norm * b_norm))


def recognize_faces():
    cv2 = _require_opencv()
    DeepFace = _require_deepface()
    if cv2 is None or DeepFace is None:
        return

    dataset_path = "dataset"
    recognized_today = set()  # Track already recognized students today
    last_recognition_time = {}  # Track last recognition time per student
    recognition_cooldown = 5  # Seconds between recognitions for same student
    
    # Try to load pre-generated embeddings first
    embeddings = load_embeddings()
    use_embeddings = embeddings is not None
    
    if not use_embeddings:
        print("No embeddings found. Using DeepFace.find (slower).")
        print("Run train.py to generate embeddings for faster recognition.")
    else:
        print(f"Loaded embeddings for {len(embeddings)} students.")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera. Please check that a webcam is connected and free.")
        return
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    print("Starting real-time recognition. Press 'q' to quit.")
    print("Face detection active...")
    
    frame_count = 0
    process_every_n_frames = 5  # Process every 5th frame for better performance
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Process recognition every N frames
        if frame_count % process_every_n_frames == 0 and len(faces) > 0:
            try:
                # Crop face region
                x, y, w, h = faces[0]
                face_roi = frame[y:y+h, x:x+w]
                
                if use_embeddings:
                    # Use pre-generated embeddings for faster recognition
                    current_embedding = DeepFace.represent(
                        img_path=face_roi,
                        model_name='Facenet',
                        enforce_detection=False
                    )
                    
                    if current_embedding:
                        current_emb = np.array(current_embedding[0]['embedding'])
                        best_match = None
                        best_distance = float('inf')
                        
                        for student_id, data in embeddings.items():
                            stored_emb = np.array(data['embedding'])
                            # Calculate cosine distance (scale-invariant)
                            distance = _cosine_distance(current_emb, stored_emb)
                            
                            if distance < best_distance:
                                best_distance = distance
                                best_match = student_id
                        print(f"Candidate {best_match} distance={best_distance:.3f}")
                        # Threshold for recognition (adjust as needed)
                        threshold = THRESHOLD
                        if best_match and best_distance < threshold:
                            student_id = best_match
                            student_name = embeddings[best_match]['name']
                            
                            # Check cooldown
                            now = datetime.datetime.now()
                            if student_id in last_recognition_time:
                                time_diff = (now - last_recognition_time[student_id]).total_seconds()
                                if time_diff < recognition_cooldown:
                                    continue
                            
                            # Mark attendance
                            date = now.strftime("%Y-%m-%d")
                            time = now.strftime("%H:%M:%S")
                            
                            if mark_attendance(student_id, date, time):
                                recognized_today.add(student_id)
                                last_recognition_time[student_id] = now
                                print(f"✓ Attendance marked: {student_name} ({student_id}) at {time}")
                                cv2.putText(frame, f"Recognized: {student_name}", (x, y-10),
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            else:
                                cv2.putText(frame, f"Already marked: {student_name}", (x, y-10),
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                        else:
                            cv2.putText(frame, "Unknown", (x, y-10),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    # Fallback to DeepFace.find
                    result = DeepFace.find(
                        img_path=face_roi,
                        db_path=dataset_path,
                        enforce_detection=False,
                        silent=True
                    )
                    
                    if result and len(result) > 0 and len(result[0]) > 0:
                        identity_path = result[0].iloc[0]['identity']
                        student_id = os.path.basename(os.path.dirname(identity_path))
                        
                        # Check cooldown
                        now = datetime.datetime.now()
                        if student_id in last_recognition_time:
                            time_diff = (now - last_recognition_time[student_id]).total_seconds()
                            if time_diff < recognition_cooldown:
                                continue
                        
                        student = get_student(student_id)
                        if student:
                            student_name = student[1]
                            date = now.strftime("%Y-%m-%d")
                            time = now.strftime("%H:%M:%S")
                            
                            if mark_attendance(student_id, date, time):
                                recognized_today.add(student_id)
                                last_recognition_time[student_id] = now
                                print(f"✓ Attendance marked: {student_name} ({student_id}) at {time}")
                                cv2.putText(frame, f"Recognized: {student_name}", (x, y-10),
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            else:
                                cv2.putText(frame, f"Already marked: {student_name}", (x, y-10),
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                        else:
                            cv2.putText(frame, "Unknown", (x, y-10),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            except Exception as e:
                # Silently continue on recognition errors
                pass
        
        cv2.imshow("Face Recognition - Press 'q' to quit", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"\nRecognition session ended. Total recognized today: {len(recognized_today)}")
