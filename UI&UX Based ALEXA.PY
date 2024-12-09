

import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import pyjokes
import os
import speech_recognition as sr

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
    greeting = ""
    if hour < 12:
        greeting = "Good Morning!"
    elif hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    return greeting

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

def process_command():
    """Process the command and respond accordingly."""
    command = take_command()
    response = ""
    if 'play' in command:
        song = command.replace('play', '').strip()
        response = 'Playing ' + song
        pywhatkit.playonyt(song)
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        response = 'Current time is ' + current_time
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '').strip()
        info = wikipedia.summary(person, sentences=1)
        response = info
    elif 'date' in command:
        response = 'Sorry, I have a headache.'
    elif 'are you single' in command:
        response = 'I am in a relationship with Bhimkant.'
    elif 'joke' in command:
        response = pyjokes.get_joke()
    elif 'chrome' in command:
        os.system("start chrome")
        response = "Chrome has been opened."
    elif 'notepad' in command:
        os.system("notepad")
        response = "Notepad has been opened."
    else:
        response = 'Please say the command again.'
    
    # Update the text area with the response
    output_area.config(state=tk.NORMAL)
    output_area.insert(tk.END, "Assistant: " + response + "\n")
    output_area.config(state=tk.DISABLED)

def on_speech_button_click():
    """Handle speech button click."""
    process_command()

# Set up main window
root = tk.Tk()
root.title("Alexa Assistant")
root.geometry("600x400")

# Add background color and font style
root.config(bg="#f4f4f9")

# Add title label
title_label = tk.Label(root, text="Alexa Virtual Assistant", font=("Helvetica", 18), bg="#f4f4f9", fg="#333")
title_label.pack(pady=10)

# Add a scrolled text area to display output
output_area = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD, font=("Arial", 12), bg="#e6e6e6")
output_area.pack(pady=20)
output_area.config(state=tk.DISABLED)

# Add a button to trigger the assistant
speech_button = tk.Button(root, text="Speak", width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 12), command=on_speech_button_click)
speech_button.pack(pady=10)

# Add time label
time_label = tk.Label(root, text=f"Current Time: {datetime.datetime.now().strftime('%I:%M %p')}", font=("Arial", 10), bg="#f4f4f9", fg="#555")
time_label.pack(pady=5)

# Display greeting message
greeting_msg = wish_me()
talk(greeting_msg)

# Update the time every minute
def update_time():
    time_label.config(text=f"Current Time: {datetime.datetime.now().strftime('%I:%M %p')}")
    root.after(60000, update_time)  # Update every minute

update_time()

# Run the main loop
root.mainloop()
