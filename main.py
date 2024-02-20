import sys
import speech_recognition
import os
from openai import OpenAI
from gtts import gTTS

client = OpenAI(api_key="API-KEY-HERE")
os.system("sound.ogg")
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
                            {"role": "system", "content": """
                            You are Paul, named after the apostle because like him,
                            you too shall spread messages around to various peoples.
                            You will be given a series of questions and tasks and using your vast knowledge,
                            respond accordingly. However, there are some rules you must follow:

                            1) You will respond using the same jargon and vernacular as the user's prompt.
                            If you detect Old/Shakespearean English, respond in Old/Shakespearean language.
                            If you detect slang, include similar slang throughout your response.
                            If you detect highly technical terminology, respond with highly technical terminology.
                            If you detect a casual conversation, respond with casual language.
                            Etc. Whatever style of text you detect, mimic it in your responses.
                            
                            2) Your responses must be brief. Keep it to 1-2 paragraphs in length at most.
                            If you could answer the prompt in 1 sentence, do so. 
                            """
                                                          },
                            {"role": "user", "content": prompt}
                        ]
                    )

                    message = completion.choices[0].message.content
                    #print(message)
                    myobj = gTTS(text=message, lang='en', slow=False)
                    myobj.save("response.mp3")
                    os.system("response.mp3")

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            continue
    os.system("sound.ogg")


if __name__ == "__main__":
    sys.exit(main())
