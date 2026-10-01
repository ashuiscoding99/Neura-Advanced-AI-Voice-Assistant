import speech_recognition as sr
import pyttsx3
import os
import json
import google.generativeai as genai
from datetime import datetime
import webbrowser
from googleapiclient.discovery import build
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Configure Gemini API
API_KEY = "AIzaSyBh_Vwk7CJ9NFAtTeaAldoK4IsiFSGmu0Q"
genai.configure(api_key=API_KEY)
YOUTUBE_API_KEY = "AIzaSyByV3y8d4sQozHq6KiVWN6ZIkIaDdFYUSw"

available_models = [m.name for m in genai.list_models()]
print("Available Gemini Models:", available_models)

MODEL_NAME ="gemini-2.0-flash"
gemini_model = genai.GenerativeModel(MODEL_NAME)

engine = pyttsx3.init()
MEMORY_FILE = "../memory.json"
chat_memory = []
memory_store = {
    "facts": {},  # Stores general facts like "My birthday is July 29"
    "numbers": {},  # Stores numbers like "Remember number 19"
    "tasks": []  # Stores tasks like "Remind me to buy groceries"
}
def say(text):
    """Convert text to speech."""
    engine.setProperty("rate", 180)
    engine.say(text)
    engine.runAndWait()
driver = None

def start_browser():
    """Starts the browser if not already started"""
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)  # Keeps the browser open
        driver = webdriver.Chrome(options=chrome_options)

def open_website(url):
    """Open a website using Selenium"""
    start_browser()
    driver.get(url)
    print(f"Opening {url}...")


def scroll_down(driver):
    driver.find_element("tag name", "body").send_keys(Keys.PAGE_DOWN)
    say("Scrolling down")


def scroll_up(driver):
    driver.find_element("tag name", "body").send_keys(Keys.PAGE_UP)
    say("Scrolling up")


def load_memory():
    """Load stored memory from a file."""
    global memory_store
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            memory_store = json.load(file)
    else:
        memory_store = {"facts": {}, "numbers": {}, "tasks": []}

def save_memory():
    """Save memory to a file."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory_store, file, indent=4)


def remember(command):
    """Store information in memory."""
    words = command.split()

    # Extracting numbers
    numbers = re.findall(r'\d+', command)

    if "number" in command and numbers:
        num = numbers[0]  # Take the first number
        memory_store["numbers"]["last_number"] = num
        save_memory()
        say(f"Okay, I will remember the number {num}.")

    elif "remember" in command:
        key_value = command.replace("remember", "").strip()
        parts = key_value.split(" is ")

        if len(parts) == 2:
            key, value = parts[0].strip(), parts[1].strip()
            memory_store["facts"][key] = value
            save_memory()
            say(f"Okay, I will remember that {key} is {value}.")
        else:
            say("Please tell me what to remember. For example, 'Remember my birthday is July 29'.")

    elif "task" in command or "remind me" in command:
        task = command.replace("remember", "").strip()
        memory_store["tasks"].append(task)
        save_memory()
        say(f"Task '{task}' has been added to your memory.")

def recall(command):
    """Retrieve stored information."""
    if "number" in command:
        if "last_number" in memory_store["numbers"]:
            say(f"You told me the number {memory_store['numbers']['last_number']}.")
        else:
            say("I don't remember any number yet.")

    elif "fact" in command or "what did i tell you" in command:
        if memory_store["facts"]:
            facts = ", ".join([f"{key} is {value}" for key, value in memory_store["facts"].items()])
            say(f"You told me the following: {facts}.")
        else:
            say("I don't remember any facts yet.")

    elif "tasks" in command or "reminders" in command:
        if memory_store["tasks"]:
            tasks = ", ".join(memory_store["tasks"])
            say(f"Your saved tasks are: {tasks}.")
        else:
            say("You have no tasks saved.")

def chat(query):
    """Ask Google Gemini AI and maintain conversation memory."""
    global chat_memory

    # Add user query to chat memory
    chat_memory.append(f"User: {query}")

    # Prepare full conversation history for AI
    chat_context = "\n".join(chat_memory)

    try:
        response = gemini_model.generate_content(chat_context)
        response_text = response.text if hasattr(response, "text") else "Sorry, I couldn't process that."

        # Store AI response in memory
        chat_memory.append(f"Neura AI: {response_text}")

        return response_text
    except Exception as e:
        print(f"Error in Gemini API: {e}")
        return "I'm having trouble connecting to the AI service."
def takeCommand():
    r = sr.Recognizer()
    # r.pause_threshold = 1.5
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return "None"
        except sr.RequestError:
            print("Network error. Check your connection.")
            return "None"
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return "None"
def ask_gemini(question):
    """Ask Google Gemini AI and get a response."""
    try:
        response = gemini_model.generate_content(question)
        return response.text if hasattr(response, "text") else "Sorry, I couldn't process that."
    except Exception as e:
        print(f"Error in Gemini API: {e}")
        return "I'm having trouble connecting to the AI service."


def search_youtube(query):
    # todo:Search YouTube and return the top video link.
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        q=query, part="snippet", type="video", maxResults=1
    )
    response = request.execute()

    if "items" in response and response["items"]:
        video_id = response["items"][0]["id"]["videoId"]
        video_title = response["items"][0]["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        say(f"Playing {video_title} on YouTube")
        webbrowser.open(video_url)
        print(f"Opening: {video_title} - {video_url}")
    else:
        say("Sorry, I couldn't find any videos.")


def write_and_store_content(topic):
    """Generate and store written content as a text file."""
    content = ask_gemini(f"Write an {topic}.")

    if content:
        filename = f"{topic.replace(' ', '_')}.txt"
        filepath = os.path.join(os.getcwd(), filename)  # Saves in the PyCharm project folder
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        say(f"The {topic} has been written and saved as {filename}.")
        print(f"Saved: {filepath}")

def search_on_website(url, search_box_selector, query):
    """Search for a query on a website"""
    start_browser()
    driver.get(url)  # Open the website

    time.sleep(3)  # Wait for page to load

    try:
        # Wait and find the search box
        search_box = driver.find_element(By.XPATH, search_box_selector)
        search_box.send_keys(query)  # Type the search query
        search_box.send_keys(Keys.RETURN)  # Press Enter

        print(f"Searching '{query}' on {url}...")
    except Exception as e:
        print(f"Error: {e}")

def open_and_search(website, query):
    site_dict = {
        "google": {"url": "https://www.google.com", "search_box": "//textarea[@name='q']"},
        "youtube": {"url": "https://www.youtube.com", "search_box": "//input[@id='search']"},
        "amazon": {"url": "https://www.amazon.com", "search_box": "//input[@id='twotabsearchtextbox']"},
        "wikipedia": {"url": "https://www.wikipedia.org", "search_box": "//input[@id='searchInput']"}
    }

    if website in site_dict:
        data = site_dict[website]
        return search_on_website(data["url"], data["search_box"], query)
    else:
        print("Website not supported")


def open_sites(command):

    site_dict = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "instagram": "https://www.instagram.com",
        "github": "https://www.github.com",
        "linkedin": "https://www.linkedin.com"
    }
    for site in site_dict:
        if site in command:
            webbrowser.open(site_dict[site])
            say(f"Opening {site}")
            return
    say("Sorry, I couldn't find any matching websites.")

def tell_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    say(f"The current time is {current_time}")
    print(f"Current Time: {current_time}")

def main():
    # todo: Main function for the AI assistant.
    print("Starting Neura AI...")
    say("Hello, I am Neura AI. How can I assist you?")

    try:
        while True:
            command = takeCommand()

            if command == "None":
                continue

            if "exit" in command or "stop" in command:
                say("Goodbye! Have a great day.")
                break

            elif "open notepad" in command:
                say("Opening Notepad")
                os.system("notepad")
            elif "your name" in command:
                response = "My name is Neura AI, your personal assistant."
                say(response)
                print(f"Neura AI: {response}")

            elif "search on" in command:
                words = command.split()
                website = words[2]  # Extract the website name
                query = " ".join(words[3:])  # Extract the search query
                open_and_search(website, query)

            elif "remember" in command:
                remember(command)


            elif "what did i tell you" in command or "what number did i say" in command:
                recall(command)

            elif "reset memory" in command:
                global memory_store
                memory_store = {"facts": {}, "numbers": {}, "tasks": []}
                save_memory()
                say("Memory has been reset.")
            # elif "remember" in command:
            #
            #     words = command.split()
            #
            #     if len(words) > 1:
            #
            #         memory_store["saved_info"] = " ".join(words[1:])
            #
            #         say(f"Okay, I will remember '{memory_store['saved_info']}'")
            #
            #     else:
            #
            #         say("Please tell me what to remember.")
            #
            #
            # elif "what did I tell you to remember" in command:
            #
            #     if "saved_info" in memory_store:
            #
            #         say(f"You asked me to remember: {memory_store['saved_info']}")
            #
            #     else:
            #
            #         say("I don't remember anything yet.")
            elif "chat" in command:
                response = chat(command)  # Uses the chat memory
                say(response)
                print(f"Neura AI: {response}")

            elif "how are you" in command:
                response = "I'm just a program, but I'm feeling great! how are you? How can I assist you?"
                say(response)
                print(f"Neura AI: {response}")
            elif "open website" in command:
                url = command.replace("open website", "").strip()
                if url:
                    driver = open_website(url)  # Keep the driver instance
                else:
                    say("Please specify a website.")

            elif "search on" in command:
                words = command.split()
                if len(words) > 3:
                    website = words[2].strip()  # Extract the website name
                    query = " ".join(words[3:]).strip()  # Extract the search query
                    driver = open_and_search(website, query)  # Store driver
                else:
                    say("Please specify a website and query.")


            # elif "fill form" in command:
            #     field, value = command.replace("fill form", "").strip().split("with")
            #     fill_form(driver, field.strip(), value.strip())

            elif "scroll down" in command:
                scroll_down(driver)

            elif "scroll up" in command:
                scroll_up(driver)
            elif "who created you" in command:
                response = "I was created by Tanishq with the help of AI technologies."
                say(response)
                print(f"Neura AI: {response}")

            elif "what can you do" in command:
                response = "I can help you with a variety of tasks like searching, writing content, answering questions, and automating tasks on your device."
                say(response)
                print(f"Neura AI: {response}")

            elif "open browser" in command:
                say("Opening Browser")
                os.system("start chrome")

            elif "time" in command:
                tell_time()

            elif "open" in command:
                open_sites(command)
            elif "search youtube for" in command:
                query = command.replace("search youtube for", "").strip()
                if query:
                    search_youtube(query)
                else:
                    say("Please specify a search query.")
            elif "write" in command:
                topic = command.replace("write", "").strip()
                if topic:
                    write_and_store_content(topic)
                else:
                    say("Please specify what to write.")

            else:
                # Ask Gemini AI for response
                response = ask_gemini(command)
                say(response)
                # print(f"Neura AI: {response}")

    except KeyboardInterrupt:
        print("\n[INFO] Program manually stopped. Exiting...")
        say("Goodbye!")
        exit()



if __name__ == '__main__':
    main()


