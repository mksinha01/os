import os
import time
import json
import datetime
import webbrowser
import pyautogui
import pyperclip
import speech_recognition as sr
import pyttsx3

# ====== Configuration ======
class Config:
    ASSISTANT_NAME = "vecna"
    WAKE_WORDS = ["hey vecna", "okay vecna", "hi vecna", "vecna"]
    VOICE_RATE = 180
    VOICE_VOLUME = 1.0
    MEMORY_FILE = "vecna_memory.json"
    
    # System paths
    APP_PATHS = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
        "notepad": "notepad",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
        "vscode": "code",
        "whatsapp": [
            f"C:\\Users\\{os.environ.get('USERNAME')}\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
            f"C:\\Users\\{os.environ.get('USERNAME')}\\AppData\\Local\\Programs\\WhatsApp\\WhatsApp.exe"
        ],
        "spotify": f"C:\\Users\\{os.environ.get('USERNAME')}\\AppData\\Roaming\\Spotify\\Spotify.exe",
        "vlc": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
        "cmd": "cmd",
        "powershell": "powershell",
        "explorer": "explorer",
        "calculator": "calc",
        "paint": "mspaint",
        "task manager": "taskmgr",
        "control panel": "control"
    }
    
    FOLDER_PATHS = {
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
        "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
        "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
        "videos": os.path.join(os.path.expanduser("~"), "Videos"),
        "music": os.path.join(os.path.expanduser("~"), "Music")
    }

# ====== Speech Engine ======
class SpeechEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', Config.VOICE_RATE)
        self.engine.setProperty('volume', Config.VOICE_VOLUME)
        
        # Get available voices and set a more natural one if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "english" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
    
    def speak(self, text):
        print(f"Vecna: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

# ====== Speech Recognition ======
class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
    
    def listen(self):
        with sr.Microphone() as source:
            print("🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        return audio
    
    def recognize(self, audio):
        try:
            text = self.recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("Network error with speech recognition")
            return ""

# ====== System Controller ======
class SystemController:
    @staticmethod
    def open_app(app_name):
        matched = [key for key in Config.APP_PATHS.keys() if key in app_name.lower()]
        if matched:
            app_key = matched[0]
            app_path = Config.APP_PATHS[app_key]
            
            # Handle multiple paths (like for WhatsApp)
            if isinstance(app_path, list):
                for path in app_path:
                    try:
                        expanded_path = os.path.expandvars(path)
                        if os.path.exists(expanded_path):
                            os.startfile(expanded_path)
                            return f"Opening {app_key}"
                    except:
                        continue
                return f"Could not find {app_key} on your system"
            else:
                try:
                    os.startfile(os.path.expandvars(app_path))
                    return f"Opening {app_key}"
                except FileNotFoundError:
                    return f"{app_key} not found on your system"
        else:
            return f"I don't know how to open {app_name}"
    
    @staticmethod
    def open_folder(folder_name):
        matched = [key for key in Config.FOLDER_PATHS.keys() if key in folder_name.lower()]
        if matched:
            folder_key = matched[0]
            try:
                os.startfile(Config.FOLDER_PATHS[folder_key])
                return f"Opening {folder_key} folder"
            except:
                return f"Could not open {folder_key} folder"
        else:
            return f"I don't know where to find {folder_name} folder"
    
    @staticmethod
    def close_window():
        pyautogui.hotkey('alt', 'f4')
        return "Closed the current window"
    
    @staticmethod
    def close_tab():
        pyautogui.hotkey('ctrl', 'w')
        return "Closed the current tab"
    
    @staticmethod
    def switch_window():
        pyautogui.hotkey('alt', 'tab')
        return "Switched to the next window"
    
    @staticmethod
    def switch_tab():
        pyautogui.hotkey('ctrl', 'tab')
        return "Switched to the next tab"
    
    @staticmethod
    def type_text(text):
        pyautogui.write(text)
        return f"Typed: {text}"
    
    @staticmethod
    def copy_text():
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)  # Wait for clipboard to update
        return pyperclip.paste()
    
    @staticmethod
    def paste_text():
        pyautogui.hotkey('ctrl', 'v')
        return "Pasted text"
    
    @staticmethod
    def select_all():
        pyautogui.hotkey('ctrl', 'a')
        return "Selected all text"
    
    @staticmethod
    def search_web(query):
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return f"Searching the web for {query}"
    
    @staticmethod
    def get_current_time():
        return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"
    
    @staticmethod
    def get_current_date():
        return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"

# ====== Command Processor ======
class CommandProcessor:
    def __init__(self, speech_engine, system_controller):
        self.speech_engine = speech_engine
        self.system = system_controller
        self.commands = {
            "open": self._handle_open,
            "close": self._handle_close,
            "type": self._handle_type,
            "write": self._handle_type,
            "copy": self._handle_copy,
            "paste": self._handle_paste,
            "select all": self._handle_select_all,
            "search for": self._handle_search,
            "google": self._handle_search,
            "what time": self.system.get_current_time,
            "what date": self.system.get_current_date,
            "what day": self.system.get_current_date,
            "switch window": self.system.switch_window,
            "switch tab": self.system.switch_tab,
        }
    
    def _handle_open(self, command):
        if "folder" in command:
            folder_name = command.replace("open", "").replace("folder", "").strip()
            return self.system.open_folder(folder_name)
        else:
            app_name = command.replace("open", "").strip()
            return self.system.open_app(app_name)
    
    def _handle_close(self, command):
        if "tab" in command:
            return self.system.close_tab()
        else:
            return self.system.close_window()
    
    def _handle_type(self, command):
        for keyword in ["type", "write"]:
            if keyword in command:
                text_to_type = command.split(keyword, 1)[1].strip()
                if not text_to_type:
                    self.speech_engine.speak("What should I type?")
                    # This would need to call the listen function
                    # text_to_type = listen_for_command()
                return self.system.type_text(text_to_type)
    
    def _handle_copy(self, command):
        selected_text = self.system.copy_text()
        return f"Copied text: {selected_text[:50]}..." if len(selected_text) > 50 else f"Copied text: {selected_text}"
    
    def _handle_paste(self, command):
        return self.system.paste_text()
    
    def _handle_select_all(self, command):
        return self.system.select_all()
    
    def _handle_search(self, command):
        query = ""
        if "search for" in command:
            query = command.split("search for", 1)[1].strip()
        elif "google" in command:
            query = command.split("google", 1)[1].strip()
        
        if query:
            return self.system.search_web(query)
        else:
            return "What would you like me to search for?"
    
    def process_command(self, command):
        for key_phrase, handler in self.commands.items():
            if key_phrase.lower() in command.lower():
                response = handler(command.lower())
                return response
        
        return "I'm not sure how to help with that. Could you rephrase your request?"

# ====== Wake Word Detection ======
class VecnaAssistant:
    def __init__(self):
        self.speech_engine = SpeechEngine()
        self.recognizer = SpeechRecognizer()
        self.system = SystemController()
        self.command_processor = CommandProcessor(self.speech_engine, self.system)
        self.wake_words = Config.WAKE_WORDS
    
    def listen_for_wake_word(self):
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                self.recognizer.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.recognizer.listen(source, phrase_time_limit=3)
            
            try:
                text = self.recognizer.recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}")
                
                for wake_word in self.wake_words:
                    if wake_word in text:
                        print(f"Wake word detected: {wake_word}")
                        return True
            
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service")
                
        except Exception as e:
            print(f"Error in wake word detection: {e}")
            time.sleep(1)
            
        return False
    
    def run(self):
        # Startup message
        self.speech_engine.speak(f"Vecna initialized. At your command.")
        
        while True:
            # Listen for wake word
            if self.listen_for_wake_word():
                # Visual/audio indication that wake word was detected
                self.speech_engine.speak("Yes?")
                
                # Listen for command
                audio = self.recognizer.listen()
                command = self.recognizer.recognize(audio)
                
                if command:
                    print(f"You said: {command}")
                    
                    # Process the command
                    response = self.command_processor.process_command(command)
                    
                    # Speak the response
                    self.speech_engine.speak(response)
                else:
                    self.speech_engine.speak("I didn't catch that. Please try again.")

# ====== Run Assistant ======
if __name__ == "__main__":
    vecna = VecnaAssistant()
    vecna.run()
