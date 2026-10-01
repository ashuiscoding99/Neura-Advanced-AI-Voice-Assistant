import eel
import os
from neura_engine.command import takecommand, speak
from neura_engine.features import (
    remember, recall, reset_memory, tell_time,
    handle_write, open_site, handle_search_on_site
)
from neura_engine.chat import ask_gemini
from neura_engine.youtube import search_youtube

def main():
    eel.init("www")
    speak("Hello, I am Neura AI. How can I assist you?")

    @eel.expose
    def run_voice():
        while True:
            command = takecommand()
            if not command or command == "none":
                eel.display_response("Sorry, I didn't catch that.")
                return

            if "exit" in command:
                speak("Goodbye!")
                eel.display_response("Goodbye!")
                return

            # Add all features here...
            response = ask_gemini(command)
            speak(response)
            eel.display_response(response)
            if not command or command == "none":
                continue

            if "exit" in command or "stop" in command:
                speak("Goodbye! Have a great day.")
                break
            elif "remember" in command:
                remember(command)
            elif "what did i tell you" in command or "what number" in command:
                recall(command)
            elif "reset memory" in command:
                reset_memory()
            elif "open notepad" in command:
                os.system("notepad")
                speak("Opening Notepad")
            elif "your name" in command:
                speak("My name is Neura AI, your personal assistant.")
            elif "how are you" in command:
                speak("I'm just a program, but I'm feeling great! How can I assist you?")
            elif "search on" in command:
                try:
                    _, _, website, *query = command.split()
                    handle_search_on_site(website, " ".join(query))
                except:
                    speak("Please specify a website and query.")
            elif "open website" in command:
                url = command.replace("open website", "").strip()
                open_site(url)
            elif "open" in command:
                open_site(command)
            elif "scroll down" in command:
                os.system("osascript -e 'tell application \"System Events\" to key code 125'")  # or use Selenium
                speak("Scrolling down")
            elif "scroll up" in command:
                os.system("osascript -e 'tell application \"System Events\" to key code 126'")
                speak("Scrolling up")
            elif "time" in command:
                tell_time()
            elif "search youtube for" in command:
                query = command.replace("search youtube for", "").strip()
                search_youtube(query)
            elif "write" in command:
                topic = command.replace("write", "").strip()
                handle_write(topic)
            elif "chat" in command:
                response = ask_gemini(command)
                speak(response)
            else:
                response = ask_gemini(command)
                speak(response)

    eel.start("index.html", size=(1000, 700))

if __name__ == '__main__':
    main()