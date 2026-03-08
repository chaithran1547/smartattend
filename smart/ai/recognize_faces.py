import cv2
import mysql.connector
from datetime import datetime
import pickle
import os
import sys

# ---------------------------
# Load trained model
# ---------------------------
BASE_DIR = os.path.dirname(__file__)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(os.path.join(BASE_DIR, "trained_model.yml"))

with open(os.path.join(BASE_DIR, "label_map.pkl"), "rb") as f:
    students = pickle.load(f)

print("Loaded students:", students)

# ---------------------------
# MySQL connection
# ---------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nomika@143",
    database="smart_attendance"
)

cursor = db.cursor()

# ---------------------------
# Face detection
# ---------------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

print("Starting camera...")

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
   
    if not ret:
        print("Camera error")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(face)

        if confidence > 70:
            name = "Unknown"
        else:
            name = students[label]

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, name, (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        if name == "Unknown":
            continue

        today = datetime.now().date()
        current_time = datetime.now().time()

        check_sql = """
        SELECT * FROM attendance
        WHERE name=%s AND date=%s
        """

        cursor.execute(check_sql, (name, today))
        result = cursor.fetchone()

        if result is None:

            insert_sql = """
            INSERT INTO attendance
            (name, date, time, status, confidence)
            VALUES (%s,%s,%s,%s,%s)
            """

            values = (name, today, current_time, "Present", confidence)

            cursor.execute(insert_sql, values)
            db.commit()

            print("✅ Attendance marked for:", name)

            # CLOSE CAMERA AND EXIT PROGRAM
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()

        else:
            print("Already marked today:", name)

    cv2.imshow("Smart Attendance", frame)

    if cv2.waitKey(1) == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
exit()