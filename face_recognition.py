import cv2
import numpy as np
import os
from insightface.app import FaceAnalysis
from numpy.linalg import norm
import time
import csv
from datetime import datetime

# --- Cosine similarity function ---
def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

# --- Brightness enhancement function ---
def enhance_brightness(image):
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

# --- Load registered face embeddings ---
def load_registered_embeddings(folder_path):
    embeddings = {}
    for file in os.listdir(folder_path):
        if file.endswith(".npy"):
            name = os.path.splitext(file)[0]
            embeddings[name] = np.load(os.path.join(folder_path, file))
    return embeddings

# --- Check if user already logged today ---
def already_logged_today(name):
    today_str = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists("access_log.csv"):
        return False
    with open("access_log.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[1] == name and today_str in row[0]:
                return True
    return False

# --- Log access attempts ---
def log_access(name, access, similarity=None):
    with open("access_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            access,
            f"{similarity:.2f}" if similarity is not None else "-"
        ])

# --- Initialize InsightFace model ---
model = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
model.prepare(ctx_id=0)

# --- Load registered users ---
embedding_dir = "embeddings"
registered_embeddings = load_registered_embeddings(embedding_dir)
print("✅ Loaded registered users:", list(registered_embeddings.keys()))

# --- Start webcam ---
cap = cv2.VideoCapture(0)
frame_id = 1
print("🎥 Webcam started. Press Ctrl+C to stop.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame.")
            break

        # Enhance brightness
        frame = enhance_brightness(frame)

        # Detect faces
        faces = model.get(frame)

        if faces:
            for face in faces:
                emb_live = face.embedding
                matched = False
                already_logged = False

                # Check known users
                for name, emb_ref in registered_embeddings.items():
                    similarity = cosine_similarity(emb_live, emb_ref)

                    if similarity > 0.35:
                        if already_logged_today(name):
                            print(f"⚠️ Skipped: {name} already logged today.")
                            matched = True
                            already_logged = True
                            break
                        label = f"Access Granted: {name}"
                        color = (0, 255, 0)
                        log_access(name, "Granted", similarity)
                        matched = True
                        break

                if not matched and not already_logged:
                    if not already_logged_today("Unknown"):
                        label = "Access Denied"
                        color = (0, 0, 255)
                        log_access("Unknown", "Denied")
                    else:
                        label = "Access Denied (Already logged)"
                        color = (0, 0, 255)
                        print("⚠️ Skipped: Unknown already logged today.")

                if not already_logged:
                    # Draw box & label
                    box = face.bbox.astype(int)
                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
                    cv2.putText(frame, label, (box[0], box[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                    # Save frame
                    output_path = f"frame_output_{frame_id}.jpg"
                    cv2.imwrite(output_path, frame)
                    print(f"✅ Saved: {output_path}")
                    frame_id += 1

        time.sleep(1)

except KeyboardInterrupt:
    print("👋 Stopping on user request.")

cap.release()
print("✅ Webcam released and finished.")
