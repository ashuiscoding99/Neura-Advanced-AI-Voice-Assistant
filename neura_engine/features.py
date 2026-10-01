from datetime import datetime
import os
from neura_engine.command import speak
from neura_engine.memory import memory_store, save_memory
from neura_engine.chat import ask_gemini
from neura_engine.youtube import search_youtube
from neura_engine.helper import get_site_info, write_content_file
from neura_engine.web_control import open_website, search_on_website

def remember(command):
    words = command.split()
    numbers = [num for num in words if num.isdigit()]

    if "number" in command and numbers:
        memory_store["numbers"]["last_number"] = numbers[0]
        save_memory()
        speak(f"Okay, I will remember the number {numbers[0]}.")

    elif "remember" in command and " is " in command:
        key, value = command.replace("remember", "").split(" is ")
        memory_store["facts"][key.strip()] = value.strip()
        save_memory()
        speak(f"Okay, I will remember that {key.strip()} is {value.strip()}.")

    elif "task" in command or "remind me" in command:
        task = command.replace("remember", "").strip()
        memory_store["tasks"].append(task)
        save_memory()
        speak(f"Task '{task}' has been added to your memory.")
    else:
        speak("Please tell me what to remember.")

def recall(command):
    if "number" in command:
        num = memory_store["numbers"].get("last_number")
        speak(f"You told me the number {num}." if num else "I don't remember any number yet.")

    elif "fact" in command or "what did i tell you" in command:
        if memory_store["facts"]:
            facts = ", ".join([f"{k} is {v}" for k, v in memory_store["facts"].items()])
            speak(f"You told me the following: {facts}.")
        else:
            speak("I don't remember any facts yet.")

    elif "tasks" in command or "reminders" in command:
        if memory_store["tasks"]:
            tasks = ", ".join(memory_store["tasks"])
            speak(f"Your saved tasks are: {tasks}.")
        else:
            speak("You have no tasks saved.")

def reset_memory():
    memory_store["facts"].clear()
    memory_store["numbers"].clear()
    memory_store["tasks"].clear()
    save_memory()
    speak("Memory has been reset.")

def tell_time():
    now = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}")

def handle_write(topic):
    content = ask_gemini(f"Write an {topic}.")
    if content:
        filename = write_content_file(topic, content)
        speak(f"The {topic} has been written and saved as {filename}.")

def open_site(command):
    url = get_site_info(command)
    if url:
        open_website(url)
        speak(f"Opening {url}")
    else:
        speak("Sorry, I couldn't find any matching websites.")

def handle_search_on_site(website, query):
    data = get_site_info(website, full=True)
    if data:
        search_on_website(data["url"], data["search_box"], query)
    else:
        speak("Website not supported.")