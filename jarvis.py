import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import requests

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level

# Function to make Jarvis speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to recognize speech input
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {command}\n")
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand. Please repeat.")
        return None
    except sr.RequestError:
        print("Request error. Check your internet.")
        return None

# Function to get weather info
def get_weather(city):
    api_key = "YOUR_API_KEY"  # Replace with OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response["cod"] == 200:
        weather = response["weather"][0]["description"]
        temperature = response["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temperature}°C."
    else:
        return "City not found."

# Main function to handle commands
def jarvis():
    speak("Hello, I am Jarvis. How can I assist you?")
    
    while True:
        command = take_command()
        if command is None:
            continue

        # Basic Commands
        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        elif "date" in command:
            today = datetime.datetime.today().strftime("%A, %B %d, %Y")
            speak(f"Today's date is {today}")

        elif "wikipedia" in command:
            speak("Searching Wikipedia...")
            command = command.replace("wikipedia", "")
            result = wikipedia.summary(command, sentences=2)
            speak("According to Wikipedia")
            speak(result)

        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif "weather" in command:
            speak("Please tell me the city name.")
            city = take_command()
            if city:
                weather_info = get_weather(city)
                speak(weather_info)

        elif "play music" in command:
            music_dir = "C:\\Users\\Public\\Music"  # Change to your music folder
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                speak("Playing music")
            else:
                speak("No music found.")

        elif "exit" in command or "stop" in command:
            speak("Goodbye! Have a great day.")
            break

        else:
            speak("Sorry, I didn't understand that.")

# Run Jarvis AI
if __name__ == "__main__":
    jarvis()
