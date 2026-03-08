import cv2
import os

student_name = input("Enter student name: ")

dataset_path = "dataset/" + student_name

if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

camera = cv2.VideoCapture(0)

count = 0

print("Press 's' to save image")
print("Press 'q' to quit")

while True:
    ret, frame = camera.read()

    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Capture Faces", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        file_path = dataset_path + "/" + str(count) + ".jpg"
        cv2.imwrite(file_path, frame)
        print("Image saved:", file_path)
        count += 1

    elif key == ord('q'):
        print("Closing camera...")
        break

camera.release()
cv2.destroyAllWindows()