import cv2
import os
import numpy as np
import pickle

dataset_path = "dataset"

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_map = {}
current_label = 0

for person_name in os.listdir(dataset_path):

    person_path = os.path.join(dataset_path, person_name)

    if not os.path.isdir(person_path):
        continue

    label_map[current_label] = person_name

    for image_name in os.listdir(person_path):

        img_path = os.path.join(person_path, image_name)

        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        detected_faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in detected_faces:

            face = gray[y:y+h, x:x+w]

            faces.append(face)
            labels.append(current_label)

    current_label += 1

recognizer.train(faces, np.array(labels))

recognizer.save("ai/trained_model.yml")

with open("ai/label_map.pkl", "wb") as f:
    pickle.dump(label_map, f)

print("Model trained successfully!")
print("Label map:", label_map)