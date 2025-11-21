import os
import pickle
from database import get_all_students
import numpy as np

def generate_embeddings():
    """
    Generate embeddings for all enrolled students and store them for quick lookup.
    This improves recognition speed significantly.
    """
    try:
        from deepface import DeepFace
    except ImportError:
        print("Error: The 'deepface' package is not installed. Install with 'pip install deepface'.")
        return False

    dataset_path = "dataset"
    models_path = "models"
    os.makedirs(models_path, exist_ok=True)
    
    embeddings = {}
    students = get_all_students()
    
    if not students:
        print("No students enrolled yet!")
        return False
    
    print("Generating embeddings for all enrolled students...")
    print("This may take a few minutes...")
    
    for student in students:
        student_id = student[2]  # student_id is at index 2
        student_name = student[1]  # name is at index 1
        student_folder = os.path.join(dataset_path, student_id)
        
        if not os.path.exists(student_folder):
            print(f"Warning: No images found for {student_name} ({student_id})")
            continue
        
        # Get all images for this student
        image_files = [f for f in os.listdir(student_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            print(f"Warning: No valid images found for {student_name} ({student_id})")
            continue
        
        # Generate embeddings for multiple images and average them
        student_embeddings = []
        for image_file in image_files[:10]:  # limit to first 10 images for speed
            image_path = os.path.join(student_folder, image_file)
            try:
                embedding = DeepFace.represent(
                    img_path=image_path,
                    model_name='Facenet',
                    enforce_detection=False
                )
                if embedding:
                    student_embeddings.append(embedding[0]['embedding'])
            except Exception as e:
                print(f"✗ Error processing {student_name} ({student_id}) - {image_file}: {str(e)}")
                continue
        
        if student_embeddings:
            mean_embedding = np.mean(student_embeddings, axis=0).tolist()
            embeddings[student_id] = {
                'name': student_name,
                'embedding': mean_embedding,
                'images_used': len(student_embeddings)
            }
            print(f"✓ Generated embedding for {student_name} ({student_id}) using {len(student_embeddings)} images")
        else:
            print(f"✗ No embeddings generated for {student_name} ({student_id}). Check image quality.")
    
    # Save embeddings to file
    embeddings_file = os.path.join(models_path, 'embeddings.pkl')
    with open(embeddings_file, 'wb') as f:
        pickle.dump(embeddings, f)
    
    print(f"\n✓ Embeddings generated and saved to {embeddings_file}")
    print(f"Total students processed: {len(embeddings)}")
    return True

def load_embeddings():
    """Load pre-generated embeddings from file."""
    embeddings_file = "models/embeddings.pkl"
    if os.path.exists(embeddings_file):
        with open(embeddings_file, 'rb') as f:
            return pickle.load(f)
    return None

if __name__ == "__main__":
    generate_embeddings()

