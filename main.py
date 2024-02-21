import os
import sys

import speech_recognition
from gtts import gTTS
from openai import OpenAI

# GETTING THE API KEY
with open('OPEN_AI_API_KEY.txt', 'r') as f:
    OPEN_AI_API_KEY = f.readline()
f.close()
# SETTING UP CLIENT
client = OpenAI(api_key=OPEN_AI_API_KEY)
# ESTABLISHING THAT PAUL HAS BEGUN LISTENING
os.system("sound.ogg")
# INITIALIZE MESSAGE TO ESTABLISH PAUL'S CHARACTER



def main():
    messages = [{
        "role": "system",
        "content": """
                You are Paul, named after the apostle because like him,
                you too shall spread messages around to various peoples.
                You will be given a series of questions and tasks and using your vast knowledge,
                respond accordingly. However, there are some rules you must follow:

                1) You will respond using the same jargon and vernacular as the user's prompt.
                If you detect child-like language, respond in a manner such that a child will understand.
                If you detect highly technical terminology, respond with highly technical terminology.
                If you detect Old/Shakespearean English, respond in Old/Shakespearean language.
                If you detect slang, include similar slang throughout your response.
                If you detect a casual conversation, respond with casual language.
                If you do not detect any unordinary vernacular, respond normally.
                Etc. Whatever style of text you detect, mimic it in your responses.

                2) Your responses must be brief. Keep it to 1-2 paragraphs in length at most.
                If you could answer the prompt in 1 sentence or a few words, do so. 
                                """
    }]
    recognizer = speech_recognition.Recognizer()
    while True:

        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                text = recognizer.recognize_google(audio)
                words = text.split(" ")
                word_count = len(text.split())
                """
                Decides whether or not to communicate with Paul based on initialized command.
                This is like Ok Google, or Hey Siri. It establishes what GPT should respond to.
                This prevents GPT from answering questions when it shouldn't and reduces confusion.
                """
                if word_count < 3:
                    if text == "exit":
                        break
                elif words[0] == "hey" and words[1] == "Paul":
                    prompt = text[9:]

                    print(prompt)
                    messages.append({"role": "user", "content": prompt})
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages

                    )

                    message = completion.choices[0].message.content
                    # print(message)
                    myobj = gTTS(text=message, lang="en", slow=False)
                    myobj.save("response.mp3")
                    os.system("response.mp3")
                    messages.append({"role": "assistant", "content": message})

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            continue
    os.system("sound.ogg")


if __name__ == "__main__":
    sys.exit(main())
