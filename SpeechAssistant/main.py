import speech_recognition as sr
import webbrowser
import playsound
import os
import random
from gtts import gTTS
from time import ctime
import time

r = sr.Recognizer()

# Constants
BOT_NAME = 'DRI Assistant'
SEARCH_URL = 'https://google.com/search?q='
MAPS_URL = 'https://google.nl/maps/place/'

def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            bot_speak(ask)
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio)
            return voice_data
        except sr.UnknownValueError:
            return 'Sorry, I did not understand.'
        except sr.RequestError:
            return 'Sorry, my speech service is down.'

def bot_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)    

def process_command(command):
    if 'what is your name' in command:
        bot_speak(f'My name is {BOT_NAME}.')
    elif 'what time is it' in command:
        bot_speak(ctime())
    elif 'search' in command:
        search_term = record_audio('What do you want to search for?')
        url = SEARCH_URL + search_term
        try:
            webbrowser.open(url)
            bot_speak(f'Here is what I found for {search_term}.')
        except webbrowser.Error:
            bot_speak('Sorry, I encountered an error while searching.')
    elif 'find location' in command:
        location = record_audio('What is the location?')
        url = MAPS_URL + location
        try:
            webbrowser.open(url)
            bot_speak(f'Here is the location of {location}.')
        except webbrowser.Error:
            bot_speak('Sorry, I encountered an error')
    elif 'exit' in command:
        exit()

time.sleep(1)
bot_speak('How can I help you?')
while 1:
    voice_data = record_audio()
    process_command(voice_data)
    