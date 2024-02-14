import sys
import speech_recognition
import pyttsx3
import pyaudio


def main():
    recognizer = speech_recognition.Recognizer()
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                text = recognizer.recognize_google(audio)
                print(text)
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            continue


if __name__ == "__main__":
    sys.exit(main())
