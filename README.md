# Neura: Your Personal AI Voice Assistant

Neura is an intelligent voice assistant designed to help you with a variety of tasks through natural language commands. Built with Python, Neura leverages Google's Gemini AI for conversational abilities, interacts with web services using Selenium, and provides a seamless hands-free experience.

## Features

* **Voice Commands**: Interact with Neura using spoken commands.
* **Conversational AI**: Powered by Google Gemini, Neura can understand and respond to your queries in a natural way.
* **Memory Management**: Neura can remember facts, numbers, and tasks you tell it, and recall them later.
    * **Remember Facts**: Store information like "my birthday is July 29."
    * **Remember Numbers**: Keep track of important numbers.
    * **Remember Tasks**: Add reminders and to-do items to your memory.
* **Web Automation**:
    * **Open Websites**: Quickly open popular websites like Google, YouTube, Amazon, Facebook, Twitter, Instagram, GitHub, and LinkedIn.
    * **Search on Websites**: Perform searches directly on supported websites (e.g., Google, YouTube, Amazon, Wikipedia).
    * **YouTube Integration**: Search for and play videos on YouTube.
    * **Browser Control**: Scroll up and down web pages.
* **Content Generation**: Ask Neura to write various types of content, which it will then save as a text file.
* **System Commands**: Open applications like Notepad.
* **Time Inquiry**: Ask Neura for the current time.

## Technologies Used

* **Python**: The core programming language.
* **`pyttsx3`**: For text-to-speech capabilities.
* **`speech_recognition`**: For converting spoken commands to text.
* **`google-generativeai`**: Integrates with Google's Gemini AI for natural language understanding and generation.
* **`google-api-python-client`**: Used for interacting with Google services like YouTube Data API.
* **`selenium`**: For web automation and browser control.
* **`eel`**: (Potentially for a future GUI or web-based interface - inferred from `command.py`)
* **`json`**: For local memory storage.
* **`webbrowser`**: For opening web pages.

## Setup and Installation

### Prerequisites

* Python 3.x
* Google Chrome browser (for Selenium web automation)
* ChromeDriver (compatible with your Chrome browser version)

### API Keys

Neura requires API keys for Google Gemini and YouTube.
* **Google Gemini API Key**: Obtain one from the Google AI Studio.
* **YouTube Data API Key**: Obtain one from the Google Cloud Console.

Place your API keys in `config.py`:

```python
# config.py
ASSISTANT_NAME = "Neura AI"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"
MODEL_NAME = "gemini-2.0-flash"
MEMORY_FILE = "memory.json"
```

## Clone the Repository (or download the files):

```bash
git clone <repository_url>  # If applicable  
cd neura-ai-assistant       # Or navigate to your project directory
```

## Install Dependencies:

```bash
pip install -r requirements.txt  # If you have a requirements.txt
# Or install individually:
pip install pyttsx3 SpeechRecognition google-generativeai google-api-python-client selenium
```

*If you're using Eel:*

```bash
pip install eel
```

## Download ChromeDriver:

* Visit the [ChromeDriver Downloads page](https://sites.google.com/a/chromium.org/chromedriver/downloads).
* Download the version that matches your installed Google Chrome browser.
* Place the `chromedriver` executable in:
  * A directory in your system's PATH, **or**
  * The same directory as your `main.py` or `maintemp.py`.

---

## How to Run

```bash
python maintemp.py
```

*Neura will greet you, and you can start issuing commands.*

---

## Usage Examples

Some commands you can give to **Neura**:

* "Neura, open Google."
* "Neura, search YouTube for cat videos."
* "Neura, remember my birthday is July 29."
* "Neura, what did I tell you to remember?"
* "Neura, remember task to buy groceries."
* "Neura, what are my tasks?"
* "Neura, what is the time?"
* "Neura, who created you?"
* "Neura, how are you?"
* "Neura, write a short story about a space adventure."
* "Neura, scroll down." *(when a browser window is open)*
* "Neura, exit."

---

## Project Structure

* `command.py`: Voice input + text-to-speech output
* `config.py`: API keys & settings
* `memory.py`: Manages saved facts, numbers, and tasks
* `youtube.py`: Handles YouTube search and playback
* `helper.py`: Utility functions (e.g., writing files, fetching info)
* `web_control.py`: Selenium-based browser automation
* `features.py`: Core features like `remember`, `recall`, `open_site`, etc.
* `chat.py`: Handles interaction with Google Gemini AI
* `maintemp.py`: Main file that connects all modules and runs the assistant

---

## Future Enhancements

* **GUI Integration** using Eel
* **Advanced Web Automation** (form filling, deep navigation)
* **Calendar Integration** for reminders and events
* **Music Control** with system or streaming players
* **Smart Home Integration** *(optional)*
* **Improved Error Handling** and better user feedback

---

## Contributing

* Contributions are welcome!
* Feel free to submit pull requests or open issues for:
  * Bugs
  * Feature suggestions
  * Documentation improvements

---

## License

**MIT License**  
This project is open-source and free to use.
