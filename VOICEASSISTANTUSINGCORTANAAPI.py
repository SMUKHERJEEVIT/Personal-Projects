import subprocess
import wolframalpha
import pyttsx3
import json
import time
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import requests
import shutil
from twilio.rest import Client
from PIL import Image, ImageTk
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
 
def greet():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Good Morning Sir!")
  
    elif hour>= 12 and hour<18:
        speak("Good Afternoon Sir!")   
  
    else:
        speak("Good Evening Sir!")  
  
    assist_name =("Jarvis 1 point o")
    speak("I am your Virtual Assistant")
    speak(assist_name)
     
def take_command():
     
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
  
    except Exception as e:
        print(e)    
        print("Sorry! I am unable to recognize your voice. Please say again!")  
        return "None"
     
    return query

def username():
    speak("What should i call you sir!")
    uname = take_command()
    while not uname:  
        speak("I didn't get that. Please tell me your name again.")
        uname = take_command()
    speak("Welcome Mister")
    speak(uname)
    columns = shutil.get_terminal_size().columns
     
    print("                      #####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    print("                      #####################".center(columns))
     
    speak("How can i Help you, Sir")
 
  
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your email id', 'your email password')
    server.sendmail('your email id', to, content)
    server.close()


if __name__ == '__main__':
    clear = lambda: os.system('cls')
     
 
    clear()
    greet()
    username()
     
    while True:
         
        query = take_command().lower()

        if 'gpt' in query:
            speak("Opening Chat GPT")
            webbrowser.open("https://chat.openai.com/")

        if 'wikipedia' in query:
            speak('Searching...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
 
        elif 'open youtube' in query:
            speak("Opening Youtube\n")
            webbrowser.open("youtube.com")
 
        elif 'open google' in query:
            speak("Opening Google\n")
            webbrowser.open("google.com")
 
        elif 'open stackoverflow' in query:
            speak("Opening Stack Over flow.Happy coding")
            webbrowser.open("stackoverflow.com")   
 
        

        elif 'time' in query:

         strTime = datetime.datetime.now().strftime("%H:%M:%S")
         speak(f"Sir, currently the time is {strTime}")
        
        elif "random number" in query:
           
           speak("Generating a random number")
           print("Generating a random number:")
           a=random.randint(1,1000)
           speak(f"The number is:{a}")
           print(f"The number is:{a}")

        elif "roll dice" in query or "roll a dice" in query:
            speak("Rolling Dice")

            def roll_dice():
             num_dice = random.randint(1, 6)  
             print(f"Rolling dice...")
             result = random.randint(1, 6)
             print("The number is:", result)

        elif 'open opera' in query:
            speak("opening opera")
            codePath = r"C:/Users/Dell/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Opera Browser.lnk"
            os.startfile(codePath)
 
        elif 'email to dhruv' in query:
            try:
                speak("What would you like to write in email?")
                content = take_command()
                to = "Receiver email address"   
                sendEmail(to, content)
                speak("Email has been sent !")
            except Exception as e:
                print(e)
                speak("Sorry Sir,I am unable to send this email!")
 
        elif 'send a mail' in query:
            try:
                speak("What would you like to write in email?")
                content = take_command()
                speak("To whom should i send?")
                to = input()    
                sendEmail(to, content)
                speak("Email has been sent !")
            except Exception as e:
                print(e)
                speak("Sorry Sir,I am unable to send this email!")

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir?")
 
        elif 'fine' in query or "good" in query:
            speak("It's good to know that your fine")
 
        elif "change my name" in query:
            query = query.replace("change my name to", "")
            assist_name = query
 
        elif "change your name" in query:
            speak("What would you like to call me, Sir ")
            assist_name = take_command()
            speak("Thanks for naming me, Sir!")
 
        elif "what's your name" in query or "What is your name" in query:
            speak("My friends call me")
            speak(assist_name)
            print("My friends call me", assist_name)
 
        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()
 
        elif "who made you" in query or "who created you" in query: 
            speak("I was created by Mister Dhruv.")
             
        elif 'joke' in query:
            speak(pyjokes.get_joke())
             
        elif "calculate" in query: 
             
            app_id = "2P9EVQ-EL6WY2PAPR"
            client = wolframalpha.Client(app_id)
            index = query.lower().split().index('calculate') 
            query = query.split()[index + 1:] 
            res = client.query(' '.join(query)) 
            answer = next(res.results).text
            print("The answer is " + answer) 
            speak("The answer is " + answer) 
 
        elif 'search' in query or 'play' in query:
             
            query = query.replace("search", "") 
            query = query.replace("play", "")          
            webbrowser.open(query) 
  
        elif "who am i" in query:
            speak("If you can talk then definitely you are a human.")
 
        elif "why you came to world" in query:
            speak("Thanks to Dhruv. Further It's a secret")
 
        elif 'power point presentation' in query or "ppt" in query:
            speak("opening Power Point presentation")
            power = r"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/PowerPoint.lnk"
            os.startfile(power)
 
        elif "who are you" in query:
            speak("I am your virtual assistant created by Mister Dhruv")
 
        elif 'reason for you' in query:
            speak("I was created as a Minor project by Mister Dhruv")
 
        elif 'change background' in query:
            ctypes.windll.user32.SystemParametersInfoW(20, 
                                                       0, 
                                                       "Location of wallpaper",
                                                       0)
            speak("Background changed successfully")
 
        elif 'news' in query:
             
            try: 
                jsonObj = urlopen('''https://newsapi.org / v1 / articles?source = the-times-of-india&sortBy = top&apiKey =\\4fdaf978fc204e7099996bcf09850996\\''')
                data = json.load(jsonObj)
                i = 1
                 
                speak('here are some top news from the times of india')
                print('''=============== TIMES OF INDIA ============'''+ '\n')
                 
                for item in data['articles']:
                     
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                 
                print(str(e))
 
         
        elif 'lock window' in query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
 
        elif 'shutdown system' in query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f')
                 
        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak("Recycle Bin Recycled")
 
        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop jarvis 1 point o from listening commands")
            a = int(take_command())
            time.sleep(a)
            print(a)
 
        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl / maps / place/" + location + "")
 
        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Jarvis Camera ", "img.jpg")
 
        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
             
        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown / h")
 
        elif "log off" in query or "sign out" in query:
            speak("Make sure all the application are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])
 
        elif "write a note" in query or 'open notepad' in query:
            speak('Opening Notepad')
            speak("What should i write, sir")
            note = take_command()
            file = open('C:/Users/Dell/Desktop/Voice Assistant using Python/Note/New Text File.txt', 'w')
            speak("Sir, Should i include date and time")
            snfm = take_command()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
         
        elif "show note" in query:
            speak("Showing Notes")
            file = open("C:/Users/Dell/Desktop/Voice Assistant using Python/Note/New Text File.txt", "r") 
            print(file.read())
            speak(file.read(6))
 
        elif "update assistant" in query:
            speak("After downloading file please replace this file with the downloaded one")
            url = '# url after uploading file'
            r = requests.get(url, stream = True)
             
            with open("Voice.py", "wb") as Pypdf:
                 
                total_length = int(r.headers.get('content-length'))
                 
                for ch in progress.bar(r.iter_content(chunk_size = 2391975),
                                       expected_size =(total_length / 1024) + 1):
                    if ch:
                      Pypdf.write(ch)
                     
       
        elif "jarvis" in query:
             
            greet()
            speak("Jarvis 1 point o is in your service Mister")
            speak(assist_name)
 
        elif "weather" in query:
             
          api_key = "d8a2e2ebc69dbf838d3ea0ade951d348"
          base_url = "http://api.openweathermap.org/data/2.5/weather?"

          speak("City name: ")
          print("City name: ")
          city_name = take_command()
          complete_url = base_url + "appid=" + api_key + "&q=" + city_name
          response = requests.get(complete_url)
          weather_data = response.json()

          if response.status_code == 200:
             main_data = weather_data["main"]
             current_temperature = main_data["temp"]
             current_pressure = main_data["pressure"]
             current_humidity = main_data["humidity"]
             weather_description = weather_data["weather"][0]["description"]

             print(f"Temperature: {current_temperature} K")
             print(f"Atmospheric pressure: {current_pressure} hPa")
             print(f"Humidity: {current_humidity}%")
             print(f"Weather description: {weather_description}")

          else:
             print(f"Error: {weather_data['message']}")
             speak("Sorry, I couldn't retrieve the weather information for the specified city.")
             
        elif "send message " in query:
                
                account_sid = 'Account Sid key'
                auth_token = 'Auth token'
                client = Client(account_sid, auth_token)
 
                message = client.messages \
                                .create(
                                    body = take_command(),
                                    from_='Sender No',
                                    to ='Receiver No'
                                )
 
                print(message.sid)
 
        elif "wikipedia" in query:
            webbrowser.open("wikipedia.com")
 
        elif "Good Morning" in query:
            speak("A warm" +query)
            speak("How are you Mister")
            speak(assist_name)
 
        
        elif "will you be my gf" in query or "will you be my bf" in query:   
            speak("I'm not sure about, may be you should give me some time")
 
        elif "how are you" in query:
            speak("I'm fine, glad you me that")
 
        elif "i love you" in query:
            speak("I am sorry, I don't")
 
        elif "what is" in query or "who is" in query:
             
            client = wolframalpha.Client("2P9EVQ-EL6WY2PAPR")
            res = client.query(query)
             
            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            except StopIteration:
                print ("No results")

    
