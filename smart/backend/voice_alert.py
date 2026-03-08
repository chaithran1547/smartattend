import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def attendance_thankyou(name):
    speak(f"Attendance marked for {name}. Thank you.")

def unknown_alarm():
    speak("Alert! Unknown person detected.")