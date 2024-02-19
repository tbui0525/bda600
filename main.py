import sys
import speech_recognition
import pyttsx3
import pyaudio
import cv2
from openai import OpenAI

client = OpenAI(api_key="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")


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
                    prompt = text[9:]
                    print(prompt)
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an assistant."},
                            {"role": "user", "content": prompt}
                        ]
                    )

                    print(completion.choices[0].message.content)




        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            continue
    print("Paul sails away")


if __name__ == "__main__":
    sys.exit(main())
