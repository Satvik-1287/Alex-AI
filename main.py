import pyttsx3
import speech_recognition as sr
from plyer import notification
import datetime
import requests
import webbrowser
import psutil
import wikipedia
import os
import sys
import pywhatkit
import pyjokes
import threading
import time
from time import sleep
import pyautogui
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtCore import QThread, pyqtSignal
from gui import Ui_MainWindow
import numpy as np
import cv2
import torch


# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon='icon.ico',
        timeout=10
    )

def notifier():
    strTime = datetime.datetime.now().strftime("%H:%M")
    notification_title = "Alex AI"
    notification_message = f"Welcome Sir, its {strTime}"
    show_notification(notification_title, notification_message)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    strTime = datetime.datetime.now().strftime("%H:%M")
    speak(f"Welcome Sir, it's {strTime}, please tell me how may I help you?")

def gui():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

def get_weather(city):
    api_key = "c4f817c5f697a7db66b52c6712bc375b"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()

    if response.status_code == 200:
        if "main" in data and "weather" in data:
            main = data["main"]
            weather = data["weather"][0]
            temperature = main["temp"]
            humidity = main["humidity"]
            description = weather["description"]

            weather_report = f"Temperature: {temperature}°C\nHumidity: {humidity}%\nDescription: {description}"
            speak(weather_report)
            print(weather_report)
        else:
            speak("Unexpected response format from the weather service.")
            print("Unexpected response format from the weather service.")
    else:
        if data.get("message"):
            speak(f"Error: {data['message']}")
            print(f"Error: {data['message']}")
        else:
            speak("Failed to retrieve weather data.")
            print("Failed to retrieve weather data.")

def search_youtube(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)
    speak("Searching YouTube")

def search_google(query):
    google_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(google_url)
    speak("Searching Google")

def get_battery_info():
    battery = psutil.sensors_battery()

    if battery.power_plugged:
        status = "Charging"
    else:
        status = "Discharging"

    percentage = battery.percent
    time_left = battery.secsleft / 60 if battery.secsleft != psutil.POWER_TIME_UNKNOWN else None

    return {
        "Status": status,
        "Percentage": percentage,
        "Time Left (minutes)": time_left
    }

def tell_battery_info():
    battery_info = get_battery_info()

    speak("Battery Information:")
    print("Battery Information:")
    speak(f"Status: {battery_info['Status']}")
    print(f"Status: {battery_info['Status']}")
    speak(f"Percentage: {battery_info['Percentage']}%")
    print(f"Percentage: {battery_info['Percentage']}%")

    if battery_info['Time Left (minutes)'] is not None:
        speak(f"Time Left: {battery_info['Time Left (minutes)']:.2f} minutes")
        print(f"Time Left: {battery_info['Time Left (minutes)']:.2f} minutes")
    else:
        speak("Time Left: Calculating...")
        print("Time Left: Calculating...")

def location_check():
    try:
        ipAdd = requests.get('https://api.ipify.org').text
        url = f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
        geo_requests = requests.get(url)
        geo_data = geo_requests.json()
        city = geo_data['city']
        country = geo_data['country']
        speak(f"Sir I am not sure, but I think we are in or near {city} city of {country} country")
    except Exception as e:
        speak("Sorry sir, due to network issue, I am not able to find where we are.")
        pass

def alarm(Timing):
    alarm_time = datetime.datetime.strptime(Timing, "%I:%M %p")
    now = datetime.datetime.now()
    alarm_hour = alarm_time.hour
    alarm_minute = alarm_time.minute

    print(f"Alarm set for {Timing}")
    speak(f"Alarm set for {Timing}")

    while True:
        now = datetime.datetime.now()
        if now.hour == alarm_hour and now.minute == alarm_minute:
            print("Time Up!")
            speak("Time Up!")
            break
        time.sleep(30)

def get_news(api_key, query=None):
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        'apiKey': api_key,
        'country': 'in',
        'q': query
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles']
        if articles:
            for article in articles[:5]:
                title = article['title']
                description = article['description']
                speak(f"Title: {title}")
                speak(f"Description: {description}")
                print(f"Title: {title}")
                print(f"Description: {description}")
        else:
            speak("No news articles found.")
    else:
        speak("Failed to retrieve news.")
        print("Failed to retrieve news.")

def get_temperature_from_google(city):
    search_url = f"https://www.google.com/search?q=temperature+in+{city}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            temperature = soup.find('span', {'class': 'wob_t'}).text
            description = soup.find('div', {'class': 'wob_dcp'}).text
            temperature_report = f"Temperature in {city}: {temperature}°C, {description}"
            return temperature_report
        except AttributeError:
            return "Could not find temperature information. Please try again."
    else:
        return "Failed to retrieve data from Google."
    
def calculate(expression):
    try:
        expression = expression.replace('x', '*').replace('X', '*').replace('times', '*').replace('divided by', '/')
        result = eval(expression)
        return result
    
    except ZeroDivisionError:
        return "Error: Division by zero"
    
    except Exception as e:
        return f"Error: {str(e)}"
    
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
    print(joke)

def object_recognition():
    speak("Sir, if you want to close object recognition, you can either say stop or close, or press the q key on your keyboard.")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/yolov5s.pt')

    # Set up video capture
    cap = cv2.VideoCapture(0)

    # Colors for each class
    np.random.seed(543210)
    colors = np.random.uniform(0, 255, size=(80, 3))

    # Set of seen objects
    seen_objects = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection
        results = model(frame)

        detections = []
        for det in results.xyxy[0]:  # xyxy format: [xmin, ymin, xmax, ymax, confidence, class]
            xmin, ymin, xmax, ymax, confidence, class_id = det
            if confidence > 0.2:  # Set confidence threshold
                class_name = model.names[int(class_id)]
                if class_name not in seen_objects:
                    detections.append(f"{class_name} ({confidence:.2f})")
                    seen_objects.add(class_name)
                    
                # Draw bounding box and label
                color = colors[int(class_id)]
                cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
                label = f"{class_name}: {confidence:.2f}%"
                cv2.putText(frame, label, (int(xmin), int(ymin) - 10 if int(ymin) > 20 else int(ymin) + 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        if detections:
            speak(f"I see a {detections}")

        # Display the frame
        cv2.imshow('Detected Objects', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):  # Press 'q' to break the loop
            break

    cap.release()
    cv2.destroyAllWindows()


class CommandThread(QThread):
    updateSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
    
    def run(self):
        notifier()
        wishMe()

        while True:
            query = takeCommand().lower()

            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'calculate' in query:
                expression = query.replace("calculate", "").strip()
                result = calculate(expression)
                speak(f"The result is {result}")
                print(f"The result is {result}")

            elif 'tell me a joke' in query:
                tell_joke()

            elif 'open youtube' in query:
                webbrowser.get('chrome').open("youtube.com")
                speak("Opening YouTube")

            elif 'close youtube' in query:
                speak("Closing Youtube")
                pyautogui.keyDown("ctrl")
                pyautogui.press("w")
                time.sleep(0.5)
                pyautogui.keyUp("ctrl")

            elif 'my name' in query:
                speak("I know that you are Satvik Sir, my developer")
                print("I know that you are Satvik Sir, my developer")

            elif 'open google' in query:
                webbrowser.get('chrome').open("google.com")
                speak("Opening Google")

            elif 'close google' in query:
                speak("Closing google")
                pyautogui.keyDown("ctrl")
                pyautogui.press("w")
                time.sleep(0.5)
                pyautogui.keyUp("ctrl")

            elif 'open spotify' in query:
                webbrowser.get('chrome').open("open.spotify.com")
                speak("Opening Spotify")

            elif 'close spotify' in query:
                speak("Closing spotify")
                pyautogui.keyDown("ctrl")
                pyautogui.press("w")
                time.sleep(0.5)
                pyautogui.keyUp("ctrl")

            elif 'open youtube music' in query or 'yt music' in query:
                webbrowser.get('chrome').open("music.youtube.com")
                speak("Opening YouTube Music")

            elif 'close youtube music' in query or 'yt music' in query:
                speak("Closing Youtube Music")
                pyautogui.keyDown("ctrl")
                pyautogui.press("w")
                time.sleep(0.5)
                pyautogui.keyUp("ctrl")

            elif 'open whatsapp' in query:
                webbrowser.get('chrome').open("web.whatsapp.com")
                speak("Opening WhatsApp")

            elif 'close whatsapp' in query:
                speak("Closing whatsapp")
                pyautogui.keyDown("ctrl")
                pyautogui.press("w")
                time.sleep(0.5)
                pyautogui.keyUp("ctrl")

            elif 'open chat gpt' in query:
                webbrowser.get('chrome').open("chatgpt.com")
                speak("Opening Chat GPT")

            elif 'close chat gpt' in query:
                speak("Closing Chat GPT")
                pyautogui.keyDown("ctrl")
                pyautogui.press("w")
                time.sleep(0.5)
                pyautogui.keyUp("ctrl")

            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

            elif 'open vs code' in query:
                codePath = "C:\\Users\\aarju\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(codePath)
                speak("Opening VS Code")

            elif 'open calculator' in query:
                os.startfile("C:\\Windows\\System32\\calc.exe")
                speak("Opening Calculator")

            elif 'sleep' in query:
                speak("Bye sir, I am going to sleep.")
                sys.exit(0)

            elif 'stop' in query or 'bye' in query:
                speak("Bye Sir.")
                pyautogui.hotkey("alt", "f4")

            elif 'battery' in query:
                tell_battery_info()

            elif 'search on youtube' in query:
                speak("Speak what you want to search.")
                queryyoutube = takeCommand()
                if queryyoutube:
                    search_youtube(queryyoutube)

            elif 'search on google' in query:
                speak("Speak what you want to search.")
                querygoogle = takeCommand()
                if querygoogle:
                    search_google(querygoogle)

            elif 'new tab' in query or 'open tab' in query or 'open a tab' in query:
                speak("OK Sir.")
                pyautogui.keyDown("ctrl")
                pyautogui.press("t")
                time.sleep(0.5)
                pyautogui.keyUp("ctrl")

            elif 'play' in query:
                song = query.replace('play', "")
                speak(f"Playing {song}")
                pywhatkit.playonyt(song)

            elif 'who is' in query:
                human = query.replace('who is', "")
                info = wikipedia.summary(human, 1)
                print(info)
                speak(info)

            elif 'weather' in query:
                speak("Speak the city name")
                city = takeCommand().lower()
                get_weather(city)

            elif 'where i am' in query or 'where we are' in query:
                location_check()

            elif 'alarm' in query:
                speak("Sir please tell me the time to set the alarm. For example, Set Alarm for 10:37 AM")
                tt = takeCommand().lower()
                tt = tt.replace("set alarm for ", "")
                tt = tt.replace(".", "")
                tt = tt.upper()
                alarm(tt)

            elif 'news' in query:
                speak("Fetching the latest news...")
                get_news(API_KEY)

            elif 'good' in query or 'perfect' in query or 'excellent' in query or 'brilliant' in query:
                speak("Sir it's my pleasure. Can I help you with anything else?")

            elif 'thankyou' in query or 'thank you' in query or 'thank' in query:
                speak("Welcome sir.")

            elif 'how are you' in query or 'how are you doing' in query or 'are you doing well' in query:
                speak("I am perfect, sir")

            elif 'switch window' in query or 'switch the window' in query:
                speak("Switching the window.")
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(0.5)
                pyautogui.keyUp("alt")

            elif 'temperature' in query:
                speak("Speak the city name")
                city = takeCommand().lower()
                temperature_report = get_temperature_from_google(city)
                print(temperature_report)
                speak(temperature_report)

            elif 'close this tab' in query or 'close tab' in query or 'close the tab' in query:
                speak("Closing the tab")
                pyautogui.keyDown("ctrl")
                pyautogui.press("w")
                time.sleep(0.5)
                pyautogui.keyUp("ctrl")

            elif 'switch tab' in query or 'switch tabs' in query or 'switch the tabs' in query or 'switch the tab' in query:
                speak("Switching the tab.")
                pyautogui.keyDown("ctrl")
                pyautogui.press("tab")
                time.sleep(0.5)
                pyautogui.keyUp("ctrl")

            # Youtube Controls
            elif 'play' in query or 'pause' in query:
                speak("OK Sir.")
                pyautogui.press("k")

            elif "mute" in query:
                speak("OK Sir")
                pyautogui.press("m")

            elif "remember that" in query:
                rememberMessage = query.replace("remember that", "")
                rememberMessage = rememberMessage.replace("alex", "")
                speak("OK Sir.")
                with open("Remember.txt", "w") as remember:
                    remember.write(rememberMessage)

            elif "what do you remember" in query:
                with open("Remember.txt", "r") as remember:
                    remember_content = remember.read()
                    if remember_content:
                        speak("You told me to remember that" + remember_content)
                    else:
                        speak("You haven't told me to remember anything yet.")

            elif "open" in query:   
                query = query.replace("open","")
                query = query.replace("alex","")
                speak("OK Sir.")
                pyautogui.press("super")
                pyautogui.typewrite(query)
                pyautogui.sleep(1)
                pyautogui.press("enter") 

            elif "screenshot" in query:
                screenshot = pyautogui.screenshot()
                screenshot.save("C:\\Users\\aarju\\OneDrive\\Pictures\\Screenshots\\screenshot.jpg")  
                speak("Sir, the screenshot is saved in the screenshots folder.")

            elif "click my photo" in query:
                pyautogui.press("super")
                pyautogui.typewrite("camera")
                pyautogui.press("enter")
                pyautogui.sleep(3)
                speak("Smile")
                pyautogui.sleep(1)
                pyautogui.press("enter")
                speak("Sir, the picture has been saved to the camera roll.")

            elif 'wifi' in query or 'wi-fi' in query:
                speak("OK Sir. But I can't work without internet, so I will not be functional.")
                pyautogui.click(1650, 1049)
                time.sleep(0.5)
                pyautogui.click(1514, 574)

            elif 'bluetooth' in query or 'blue tooth' in query:
                speak("OK Sir.")
                pyautogui.click(1650, 1049)
                time.sleep(0.5)
                pyautogui.click(1650, 571)

            elif 'desktop' in query:
                speak("OK Sir.")       
                pyautogui.keyDown('winleft')
                pyautogui.press('d')
                pyautogui.keyUp('winleft')

            elif 'close this app' in query or 'close app' in query or 'close the app' in query:
                speak("OK Sir.")       
                pyautogui.hotkey('alt', 'f4')

            elif 'detect object' in query or 'recognise object' in query or 'detect objects' in query or 'recognise objects' in query or 'object recognition' in query or 'object detection' in query or 'detect from camera' in query or 'see from camera' in query or 'recognise from camera' in query:
                object_recognition()

            elif 'increase brightness' in query or 'make my display bright' in query or 'brightness to high' in query:
                speak("OK Sir.")
                pyautogui.click(1650, 1049)
                time.sleep(0.5)
                pyautogui.click(1826, 816)
                pyautogui.click(1650, 1049)

            elif 'decrease brightness' in query or 'make my display less bright' in query or 'brightness to low' in query:
                speak("OK Sir.")
                pyautogui.click(1650, 1049)
                time.sleep(0.5)
                pyautogui.click(1596, 815)
                pyautogui.click(1650, 1049)

            elif 'normal brightness' in query or 'make my display normal bright' in query or 'brightness to normal' in query:
                speak("OK Sir.")
                pyautogui.click(1650, 1049)
                time.sleep(0.5)
                pyautogui.click(1682, 815)
                pyautogui.click(1650, 1049)

            elif 'increase volume' in query or 'volume loud' in query or 'volume to high' in query:
                speak("OK Sir.")
                pyautogui.click(1650, 1049)
                time.sleep(0.5)
                pyautogui.click(1818, 890)
                pyautogui.click(1650, 1049)

            elif 'decrease volume' in query or 'volume not loud' in query or 'volume to low' in query:
                speak("OK Sir.")
                pyautogui.click(1650, 1049)
                time.sleep(0.5)
                pyautogui.click(1625, 890)
                pyautogui.click(1650, 1049)

            elif 'normal volume' in query or 'volume normal' in query or 'volume to normal' in query:
                speak("OK Sir.")
                pyautogui.click(1650, 1049)
                time.sleep(0.5)
                pyautogui.click(1737, 890)
                pyautogui.click(1650, 1049)

            else:
                pass 

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.command_thread = CommandThread()
        self.command_thread.start()

def gui():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    API_KEY = 'f417c199f87d4c32ba4d3f36e150e850'  # news api
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    
    
    gui()