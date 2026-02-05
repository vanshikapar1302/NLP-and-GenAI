from datetime import datetime
import webbrowser
import requests
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        audio = rec.listen(source)

    try:
        query = rec.recognize_google(audio)
        print("You :", query)
        return query.lower()

    except:
        speak("Sorry, I didn't catch that")
        return ""

def get_news():
    speak("Fetching top news headlines")
    URL = "https://newsapi.org/v2/top-headlines?country=us&apiKey=695e07af402f4b119f0703e9b19f4683"

    response = requests.get(URL)
    data = response.json()

    articles = data.get("articles", [])

    for i in range(5):
        title = articles[i]['title']
        print(title)
        speak(title)

def get_location():
    URL = "http://ip-api.com/json/"
    response = requests.get(URL)
    return response.json()

def get_weather(city):
    API_KEY = "cbc3b839aeb35319c10fbf5d0fc81d09"
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(URL)
    return response.json()

def show_weather(weather):
    temp = weather['main']['temp']
    desc = weather['weather'][0]['description']

    speak(f"The temperature is {temp} degree Celsius")
    speak(f"Weather condition is {desc}")

speak("Hello! I am your voice assistant")

chat = True

while chat:
    user_msg = listen()

    if "hello" in user_msg or "hi" in user_msg:
        speak("Hello user, how can I help you?")

    elif "date" in user_msg:
        today = datetime.now().date()
        speak(f"Today's date is {today}")

    elif "time" in user_msg:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"Current time is {current_time}")

    elif "open google" in user_msg:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open" in user_msg:
        website_name = user_msg.split()[-1]
        speak(f"Opening {website_name}")
        webbrowser.open(f"https://www.{website_name}.com")

    elif "news" in user_msg:
        get_news()

    elif "weather" in user_msg:
        speak("Detecting your city")
        location = get_location()
        city = location['city']
        speak(f"Your city is {city}")
        weather = get_weather(city)
        show_weather(weather)

    elif "bye" in user_msg:
        speak("Goodbye! Have a nice day")
        chat = False

    else:
        speak("Sorry, I don't understand that command")
