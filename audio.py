import speech_recognition as sr
from pynput.keyboard import Key, Controller
import time

def main():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Please say Something..")

        audio = r.listen(source)

        try:
            keyboard = Controller()
            time.sleep(2)
            for char in r.recognize_google(audio):
                keyboard.press(char)
                keyboard.release(char)
                time.sleep(0.12)

        except Exception as e:
            print("Error :" + str(e))



if __name__ == "__main__":
    main()