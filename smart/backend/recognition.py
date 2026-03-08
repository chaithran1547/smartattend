import cv2

def start_camera():

    camera = cv2.VideoCapture(1)

    while True:

        ret, frame = camera.read()

        cv2.imshow("Smart Attendance Camera", frame)

        if cv2.waitKey(1) == 27:
            break

    camera.release()
    cv2.destroyAllWindows()