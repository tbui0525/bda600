import sys
import speech_recognition
import pyttsx3
import pyaudio
import cv2


def main():
    recognizer = speech_recognition.Recognizer()
    while True:

        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                text = recognizer.recognize_google(audio)
                words = text.split(" ")
                word_count = len(text.split())
                if word_count < 3:
                    if text == "exit":
                        break
                elif words[0] == "hey" and words[1] == "Paul":
                    print(text[9:])


        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            continue
    print("Paul sails away")


if __name__ == "__main__":
    sys.exit(main())
