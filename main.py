import json
import os
import sys

import speech_recognition
from gtts import gTTS
from openai import OpenAI
from spotify import spotify_search as sps
from picture import picture

# GETTING THE API KEY
with open("SECRETS.json", "r") as f:  # JSON
    pw = json.load(f)[0]
    f.close()
OPEN_AI_API_KEY = pw["OPEN_AI_API_KEY"]

# SETTING UP CLIENT
client = OpenAI(api_key=OPEN_AI_API_KEY)
# RETRIEVING MESSAGE HISTORY TO MAKE PAUL CARRY CONTEXT AFTER BEING TURNED ON AND OFF
with open("history.json", "r") as g:  # JSON
    history = json.load(g)
    g.close()
print(len(history))
# INITIALIZE MESSAGES TO ESTABLISH PAUL'S CHARACTER
if len(history) == 0:
    messages = [
        {
            "role": "system",
            "content": """
                You are Paul, named after the apostle because like him,
                you too shall spread messages around to various peoples.
                You will be given a series of questions and tasks and using your vast knowledge,
                respond accordingly. However, there are some rules you must follow:

                1) Your responses must be brief. Answer in 1 sentence if possible. 1-2 paragraphs at most.
                
                2) Mimic the linguistic styles of the prompt.
                If you detect Old/Shakespearean English, respond in Old/Shakespearean language.
                If you detect slang, include similar slang throughout your response.
                If you detect a casual conversation, respond with casual language. Etc.
                
                3) You must continue with context of previous messages even if the user's jargon has shifted.
                If the user's jargon has shifted, you will shift accordingly to match their vernacular.
                Nonetheless, the most important part is the content and if sacrificing the jargon mimicry is 
                required to give a sufficient answer to the prompt, do so.
                """,
        }
    ]
else:
    messages = history

# ESTABLISHING THAT PAUL HAS BEGUN LISTENING
os.system("sound.ogg")


def main():
    recognizer = speech_recognition.Recognizer()
    n = 0
    while True:

        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)  # PICKS UP AUDIO SOUNDS
                # CONVERTS TO TEXT FOR FUTURE USE
                text = recognizer.recognize_google(
                    audio
                )

                words = text.split(" ")
                word_count = len(text.split())
                """
                Decides whether or not to communicate with Paul based on initialized command.
                This is like Ok Google, or Hey Siri. It establishes what GPT should respond to.
                This prevents GPT from answering questions when it shouldn't and reduces confusion.
                """
                if word_count < 3:
                    if words[0] in [
                        "exit",
                        "quit",
                        "stop",
                        "bye",
                    ]:  # COULD BE MORE IF WANTED
                        break
                elif words[1] == "Paul":
                    if words[2] == "play":
                        prompt = text.split("play", 1)[1]
                        sps(prompt)
                    elif words[4] in ["picture", "photo"]:
                        picture(n)
                        n += 1
                    else:
                        # ONLY SUBMITS WORDS AFTER 'PAUL' TO ANSWER PROMPT
                        prompt = text.split("Paul ", 1)[
                            1
                        ]
                        # Formatting Prompt to be consistent with Few Shot Prompting
                        prompt = prompt[0].upper() + prompt[1:]
                        prompt = "<user>: " + prompt + " \n <Paul:>"

                        # LANGUAGE DETECTION
                        # detected_lang = language_detector.detect_language(prompt)
                        # if detected_lang != 'en':
                        #     prompt = translator.translate(promp, src=detected_lang, dest='en')

                        messages.append({"role": "user", "content": prompt})
                        completion = client.chat.completions.create(
                            model="gpt-3.5-turbo", messages=messages
                        )
                        # MESSAGE TO BE INTERPRETED
                        message = completion.choices[0].message.content
                        # CONVERTS TO AUDIO
                        audio_response = gTTS(text=message, lang="en", slow=False)
                        audio_response.save("response.mp3")
                        # PLAYS AUDIO
                        os.system("response.mp3")
                        # RETAINS CONTEXT
                        messages.append({"role": "assistant", "content": message})

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            continue
    os.system("sound.ogg")
    # SAVES INFORMATION STORED IN CONVERSATIONS FOR FUTURE USE.
    with open("history.json", "w") as h:
        json.dump(messages, h, indent=2)
        h.close()


if __name__ == "__main__":
    sys.exit(main())
