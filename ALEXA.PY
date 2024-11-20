import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os

# Initialize speech recognition and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def wish_me():
    """Greet the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        talk("Good Morning")
    elif hour < 18:
        talk("Good Afternoon!")
    else:
        talk("Good Evening!")
    talk("I am Alexa, what can I help you with?")

def take_command():
    """Listen for a command and return it."""
    command = ""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
                print(command)
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError:
        print("Could not request results; check your internet connection.")
    return command

def run_alexa():
    """Process the command and respond accordingly."""
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('Playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + current_time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '').strip()
        info = wikipedia.summary(person, sentences=1)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('Sorry, I have a headache.')
    elif 'are you single' in command:
        talk('I am in a relationship with Bhimkant.')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'chrome' in command:
        os.system("start chrome")
        talk("Chrome has been opened.")
    elif 'notepad' in command:
        os.system("notepad")
        talk("Notepad has been opened.")
    else:
        talk('Please say the command again.')

# Main execution loop
wish_me()
run_alexa()
# while True:
#     run_alexa()
