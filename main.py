import site
from typing import NoReturn
import speech_recognition as sr
import os
from googlesearch import search
from google import genai
from config import apikey
import webbrowser
import datetime
import time
import pywhatkit
import keyboard
import pyttsx3
import json





def say(text):          #for windows | comment this 6 line if this code not work on mac
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

#  Globals

user_name = "User"
assistant_paused = False
muted = False
last_song = ""
last_active = time.time()


# Wake word & auto-sleep settings

ASSISTANT_NAME = "chatbot"     # say "assistant_name" to wake up
SLEEP_AFTER = 59              # seconds of inactivity before sleeping

assistant_awake = False
last_active_time = time.time()


def handle_command(command):
    global user_name, assistant_paused, muted, last_song


def takeCommand(timeout=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        try:
            print("Recognizing...")
            audio = r.listen(source, timeout=timeout, phrase_time_limit=6)
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            return ""
        except Exception:
            return ""



# Make sure this is outside the function
client = genai.Client(api_key=apikey)
chatStr = ""


def chat(query):
    global chatStr
    try:
        # 1. Update the chat history string
        chatStr += f"User: {query}\nAssistant: "

        # 2. Use the correct Google GenAI syntax
        # We use 'gemini-1.5-flash' (Davinci is an old OpenAI model)
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=chatStr
        )

        # 3. Correct way to get the text from Google's response
        result_text = response.text

        # 4. Speak and update history
        print(f"AI: {result_text}")
        say(result_text)
        chatStr += f"{result_text}\n"

        return result_text

    except Exception as e:
        print(f"Error in chat: {e}")
        if "429" in str(e):
            return "I'm a bit overwhelmed, please wait a moment."
        return "I'm having trouble thinking right now."


# Setup API key
def ai(prompt):
    try:
        # 1. Generate content using Gemini
        # 'text-davinci-003' is an old OpenAI model; we use 'gemini-1.5-flash' here
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        ai_text = response.text
        full_output = f"GenAI response for Prompt: {prompt} \n *************************\n\n{ai_text}"

        # 2. Ensure the directory exists
        if not os.path.exists("genai"):
            os.mkdir("genai")

        # 3. Safe Filename Logic
        safe_name = "".join(x for x in prompt[:20] if x.isalnum() or x in "._- ").strip()
        file_path = f"genai/{safe_name}.txt"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_output)

        print(f"Response saved to {file_path}")
        return ai_text

    except Exception as e:
        print(f"An error occurred in the AI function: {e}")
        return "I encountered an error while processing that request."



def open_software(app_name):
    # List of common install directories
    search_paths = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        r"C:\Users",
        os.path.expandvars(r"%LOCALAPPDATA%"),
        os.path.expandvars(r"%APPDATA%")
    ]

    app_name = app_name.lower()

    for base in search_paths:
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.lower().startswith(app_name) and file.lower().endswith(".exe"):
                    full_path = os.path.join(root, file)
                    os.system(f'start "" "{full_path}"')
                    return True

    return False


if __name__ == '__main__':

    from website_manager import WebsiteManager  # If you put class in another file
    websites = WebsiteManager("websites.json")
    print("Hello I am your AI assistant")
    say("Hello I am your AI assistant")

    while True:

        # Auto-sleep function
        if assistant_awake and (time.time() - last_active_time > SLEEP_AFTER):
            assistant_awake = False
            say("Going to sleep.")
            print("Assistant sleeping...")

        print("Listening...")
        query = takeCommand()

        if not query:
            continue

        #  Wake Word Detection

        if not assistant_awake:
            if ASSISTANT_NAME in query:
                assistant_awake = True
                last_active_time = time.time()
                print("Yes, how can I help you?")
                say("Yes, how can I help you?")

            continue                            # ignore commands until wake word is said

            # Update activity time

        last_active_time = time.time()




        if "open" in query.lower():
            site = query.lower().replace("open", "").strip()
            say(f"Opening {site}...")

            if websites.open_website(site):
                say(f"{site} opened.")
                pass
            else:
                say("Official website not found in database.")

        elif query.lower().startswith("open app "):
            app = query.lower().replace("open app", "").strip()
            say(f"Opening {app}...")

            if not open_software(app):
                say(f"Sorry, {app} is not installed or could not be found.")
                pass

        elif "Assistant mute" in query:
            muted = True
            say("Assistant muted.")
            pass


        elif "Assistant unmute" in query:
            muted = False
            say("Assistant unmuted.")
            pass


        elif "play" in query:
            song = query.replace("play", "").strip()
            last_song = song
            say(f"Playing {song}")
            pywhatkit.playonyt(song)
            pass


        elif "pause song" in query or "pause the song" in query or "stop the song" in query or "stop" in query:
            say("Pausing the song")
            keyboard.press_and_release("space")
            pass


        elif "resume song" in query or "play the song" in query or "start the song" in query or "resume the song" in query or "start" in query:
            say("Resuming the song")
            keyboard.press_and_release("space")
            pass


        elif "mute song" in query or "mute the song" in query or "mute" in query or "unmute song" in query or "unmute the song" in query or "unmute" in query:
            say("o k")
            keyboard.press_and_release("m")
            pass


        elif "previous video" in query or "play previous video" in query or "previous" in query:
            say("playing previous video")
            keyboard.press_and_release("Shift+p")
            pass


        elif "next video" in query or "play next video" in query or "next" in query:
            say("playing next video")
            keyboard.press_and_release("Shift+n")
            pass


        elif "close the tab" in query or "close tab" in query or "close" in query:
            say("the tab is closed")
            keyboard.press_and_release("Ctrl+w")
            pass


        elif "full screen" in query or "full screen mood" in query or "full display" in query or "exit full screen" in query or "exit full display" in query or "exit full screen" in query:
            say("o k")
            keyboard.press_and_release("f")
            pass


        elif "mini mood" in query or "mini display" in query or "exit mini mood" in query or "exit mini display" in query:
            say("o k")
            keyboard.press_and_release("i")
            pass


        elif "theater mood" in query or "exit theater mood" in query or "exit theatre mood" in query or "theatre mood" in query:
            say("o k")
            keyboard.press_and_release("t")
            pass


        elif "music" in query:
            musicPath = "https://music.youtube.com"
            os.system(f"start {musicPath}")
            pass


        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            print(f"The time is {hour} hour and {min} minute.")
            say(f"The time is {hour} hour and {min} minute.")


        elif "Using ai".lower() in query.lower():
            ai(prompt=query)

            if "chatbot Quit".lower() in query.lower():
                exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""


        # If the query doesn't match specific commands above, ask Gemini
        else:
            print("Thinking...")
            ai_response = ai(query)

            # Print response for long text (like applications)
            print(f"AI: {ai_response}")

            # Speak a summarized version or the whole response
            # Note: For very long text, you might want to only speak the first few sentences
            say(ai_response)
