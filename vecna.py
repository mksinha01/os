import os
import time
import json
import random
import datetime
import webbrowser
import subprocess
import requests
import threading
import pyautogui
import pyperclip
import speech_recognition as sr
import pyttsx3
from pathlib import Path
import psutil
import pygetwindow as gw
import keyboard
import screen_brightness_control as sbc
import sys

# Optional imports - will be installed if needed
try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# ====== Configuration ======
class Config:
    ASSISTANT_NAME = "vecna"
    WAKE_WORDS = ["hey vecna", "okay vecna", "hi vecna", "vecna"]
    VOICE_RATE = 180
    VOICE_VOLUME = 1.0
    MEMORY_FILE = "vecna_memory.json"
    OFFLINE_MODE = False
    USE_WHISPER = WHISPER_AVAILABLE
    WHISPER_MODEL = "base"  # Changed from tiny to base for better accuracy - options: tiny, base, small, medium, large
    LANGUAGE = "en-US"       # Explicitly set language to US English
    USE_LLM = True
    LLM_TYPE = "openai"  # openai, gemini, ollama
    
    # API Keys
    OPENAI_API_KEY = ""  # Your OpenAI API key
    GEMINI_API_KEY = ""  # Your Gemini API key
    ELEVENLABS_API_KEY = ""  # Your ElevenLabs API key
    
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

# ====== Memory System ======
class Memory:
    def __init__(self, memory_file=Config.MEMORY_FILE):
        self.memory_file = memory_file
        self.memories = self._load_memory()
        
    def _load_memory(self):
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            else:
                return {
                    "conversations": [],
                    "preferences": {},
                    "reminders": [],
                    "custom_commands": {}
                }
        except Exception as e:
            print(f"Error loading memory: {e}")
            return {
                "conversations": [],
                "preferences": {},
                "reminders": [],
                "custom_commands": {}
            }
    
    def save_memory(self):
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memories, f, indent=4)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def add_conversation(self, user_input, assistant_response):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.memories["conversations"].append({
            "timestamp": timestamp,
            "user_input": user_input,
            "assistant_response": assistant_response
        })
        if len(self.memories["conversations"]) > 100:  # Keep only last 100 conversations
            self.memories["conversations"] = self.memories["conversations"][-100:]
        self.save_memory()
    
    def add_preference(self, key, value):
        self.memories["preferences"][key] = value
        self.save_memory()
    
    def get_preference(self, key, default=None):
        return self.memories["preferences"].get(key, default)
    
    def add_reminder(self, text, time):
        self.memories["reminders"].append({
            "text": text,
            "time": time,
            "completed": False
        })
        self.save_memory()
    
    def get_pending_reminders(self):
        now = datetime.datetime.now()
        pending = []
        for reminder in self.memories["reminders"]:
            if not reminder["completed"]:
                reminder_time = datetime.datetime.fromisoformat(reminder["time"])
                if reminder_time <= now:
                    pending.append(reminder)
                    reminder["completed"] = True
        self.save_memory()
        return pending

    def add_custom_command(self, command_name, action):
        self.memories["custom_commands"][command_name] = action
        self.save_memory()

    def get_custom_command(self, command_name):
        return self.memories["custom_commands"].get(command_name)

# ====== Speech Engine ======
class SpeechEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', Config.VOICE_RATE)
        self.engine.setProperty('volume', Config.VOICE_VOLUME)
        
        # Get available voices and set a more natural one if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "english" in voice.name.lower() and "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
    
    def speak(self, text):
        print(f"Vecna: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def configure_voice(self, rate=None, volume=None, voice_id=None):
        if rate is not None:
            self.engine.setProperty('rate', rate)
        if volume is not None:
            self.engine.setProperty('volume', volume)
        if voice_id is not None:
            self.engine.setProperty('voice', voice_id)

# ====== Speech Recognition ======
class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Lower energy threshold for better sensitivity
        self.recognizer.energy_threshold = 3000
        self.recognizer.dynamic_energy_threshold = True
        # Increase the pause threshold to give more time to finish speaking
        self.recognizer.pause_threshold = 0.8
        # Add a small amount of ambient noise adjustment
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        # Increase the timeout duration
        self.phrase_timeout = 3
        
        # Initialize Whisper if available (much better for accented English)
        self.whisper_model = None
        if Config.USE_WHISPER and WHISPER_AVAILABLE:
            try:
                # Prefer 'base' or 'small' model for better English recognition
                preferred_model = "base" if Config.WHISPER_MODEL == "tiny" else Config.WHISPER_MODEL
                self.whisper_model = WhisperModel(preferred_model, device="cpu", language="en")
                print(f"Initialized Whisper with {preferred_model} model specifically for English")
            except Exception as e:
                print(f"Error initializing Whisper: {e}")
    
    def listen(self):
        with sr.Microphone() as source:
            print("🎤 Listening...")
            # Longer adjustment for better calibration
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                print("Speak now...")
                # Increase timeout for those who speak more slowly
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=self.phrase_timeout)
                print("Processing speech...")
                return audio
            except sr.WaitTimeoutError:
                print("No speech detected")
                return None
    
    def recognize(self, audio):
        if audio is None:
            return ""
            
        # Try multiple recognition methods in order of accuracy
        text = ""
        
        # First try Whisper if available (best for accents)
        if not Config.OFFLINE_MODE and WHISPER_AVAILABLE and self.whisper_model:
            try:
                temp_file = "temp_audio.wav"
                with open(temp_file, "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Use more aggressive beam search for better accuracy
                segments, _ = self.whisper_model.transcribe(temp_file, beam_size=5, language="en")
                text = " ".join([segment.text for segment in segments])
                
                # Clean up
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                
                if text.strip():
                    print(f"Whisper recognized: '{text}'")
                    return text
            except Exception as e:
                print(f"Error with Whisper recognition: {e}")
                # Fall through to next method
        
        # Then try Google (with language explicitly set to English)
        if not text:
            try:
                # Explicitly set to English for better recognition
                text = self.recognizer.recognize_google(audio, language='en-US')
                print(f"Google recognized: '{text}'")
                return text
            except sr.UnknownValueError:
                print("Google couldn't understand audio")
            except sr.RequestError:
                print("Network error with Google recognition")
                Config.OFFLINE_MODE = True
        
        # If all methods failed
        return text or ""

# ====== System Controller ======
class SystemController:
    @staticmethod
    def open_app(app_name):
        # Enhanced app detection with more applications
        enhanced_apps = {
            "whatsapp": ["C:\\Users\\%USERNAME%\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
                        "C:\\Program Files\\WhatsApp\\WhatsApp.exe",
                        "C:\\Program Files (x86)\\WhatsApp\\WhatsApp.exe"],
            "davinci": ["C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\Resolve.exe",
                       "C:\\Program Files (x86)\\Blackmagic Design\\DaVinci Resolve\\Resolve.exe"],
            "davinci resolve": ["C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\Resolve.exe"],
            "telegram": ["C:\\Users\\%USERNAME%\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe"],
            "discord": ["C:\\Users\\%USERNAME%\\AppData\\Local\\Discord\\app-*\\Discord.exe"],
            "spotify": ["C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe"],
            "steam": ["C:\\Program Files (x86)\\Steam\\steam.exe"],
            "zoom": ["C:\\Users\\%USERNAME%\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"],
            "teams": ["C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe"],
            "vlc": ["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"],
            "obs": ["C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe"],
            "photoshop": ["C:\\Program Files\\Adobe\\Adobe Photoshop *\\Photoshop.exe"],
            "premiere": ["C:\\Program Files\\Adobe\\Adobe Premiere Pro *\\Adobe Premiere Pro.exe"],
            "after effects": ["C:\\Program Files\\Adobe\\Adobe After Effects *\\Support Files\\AfterFX.exe"],
            "blender": ["C:\\Program Files\\Blender Foundation\\Blender *\\blender.exe"],
            "unity": ["C:\\Program Files\\Unity\\Hub\\Editor\\*\\Editor\\Unity.exe"],
            "visual studio": ["C:\\Program Files\\Microsoft Visual Studio\\*\\*\\Common7\\IDE\\devenv.exe"],
            "firefox": ["C:\\Program Files\\Mozilla Firefox\\firefox.exe"],
            "edge": ["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"],
            "brave": ["C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"]
        }
        
        # Merge with existing app paths
        all_apps = {**Config.APP_PATHS, **enhanced_apps}
        
        matched = [key for key in all_apps.keys() if key in app_name.lower()]
        if matched:
            app_key = matched[0]
            app_paths = all_apps[app_key]
            
            # Handle multiple paths
            if isinstance(app_paths, list):
                for path in app_paths:
                    try:
                        expanded_path = os.path.expandvars(path)
                        # Handle wildcard paths
                        if '*' in expanded_path:
                            import glob
                            matching_paths = glob.glob(expanded_path)
                            if matching_paths:
                                os.startfile(matching_paths[0])
                                return f"Opening {app_key}"
                        elif os.path.exists(expanded_path):
                            os.startfile(expanded_path)
                            return f"Opening {app_key}"
                    except Exception as e:
                        print(f"Failed to open {path}: {e}")
                        continue
                
                # If no direct path worked, try using Windows search
                try:
                    subprocess.run(f'start "" "{app_key}"', shell=True)
                    return f"Attempting to open {app_key}"
                except:
                    return f"Could not find {app_key}"
            else:
                # Single path
                try:
                    expanded_path = os.path.expandvars(app_paths)
                    if os.path.exists(expanded_path):
                        os.startfile(expanded_path)
                        return f"Opening {app_key}"
                    else:
                        subprocess.run(f'start "" "{app_key}"', shell=True)
                        return f"Attempting to open {app_key}"
                except Exception as e:
                    return f"Error opening {app_key}: {e}"
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
    def undo():
        pyautogui.hotkey('ctrl', 'z')
        return "Undoing last action"
    
    @staticmethod
    def search_web(query):
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return f"Searching the web for {query}"
    
    @staticmethod
    def take_screenshot():
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Ensure the pictures directory exists
        pictures_dir = Config.FOLDER_PATHS["pictures"]
        os.makedirs(pictures_dir, exist_ok=True)
        screenshot_path = os.path.join(pictures_dir, f"screenshot_{timestamp}.png")
        pyautogui.screenshot(screenshot_path)
        return f"Screenshot saved to {screenshot_path}"
    
    @staticmethod
    def get_system_info():
        cpu = f"CPU usage: {psutil.cpu_percent()}%"
        ram = f"RAM usage: {psutil.virtual_memory().percent}%"
        disk = f"Disk usage: {psutil.disk_usage('/').percent}%"
        battery = ""
        if hasattr(psutil, "sensors_battery"):
            battery_info = psutil.sensors_battery()
            if battery_info:
                battery = f"Battery: {battery_info.percent}%"
        
        return f"{cpu}, {ram}, {disk} {battery}"
    
    @staticmethod
    def set_volume(level):
        # Convert level 0-100 to 0-1.0 for pyautogui
        try:
            level = min(100, max(0, int(level)))
            # Use keyboard to control volume
            current = 50  # Assume middle volume
            steps = abs(level - current) // 2  # Each key press is ~2%
            
            if level > current:
                for _ in range(steps):
                    keyboard.press_and_release('volume up')
                    time.sleep(0.1)
            else:
                for _ in range(steps):
                    keyboard.press_and_release('volume down')
                    time.sleep(0.1)
            
            return f"Volume set to approximately {level}%"
        except:
            return "Could not adjust volume"
    
    @staticmethod
    def set_brightness(level):
        try:
            level = min(100, max(0, int(level)))
            sbc.set_brightness(level)
            return f"Brightness set to {level}%"
        except:
            return "Could not adjust brightness"
    
    @staticmethod
    def play_pause_media():
        keyboard.press_and_release('play/pause media')
        return "Toggled media playback"
    
    @staticmethod
    def next_track():
        keyboard.press_and_release('next track')
        return "Skipped to next track"
    
    @staticmethod
    def previous_track():
        keyboard.press_and_release('previous track')
        return "Went back to previous track"
    
    @staticmethod
    def lock_computer():
        pyautogui.hotkey('win', 'l')
        return "Locking your computer"
    
    @staticmethod
    def get_current_time():
        return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"
    
    @staticmethod
    def get_current_date():
        return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
    
    @staticmethod
    def shutdown_computer():
        os.system("shutdown /s /t 5")
        return "Shutting down computer in 5 seconds"
    
    @staticmethod
    def restart_computer():
        os.system("shutdown /r /t 5")
        return "Restarting computer in 5 seconds"
    
    @staticmethod
    def sleep_computer():
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting computer to sleep"

# ====== Intelligence Module ======
class Intelligence:
    def __init__(self, memory):
        self.memory = memory
        self.openai_client = None
        self.gemini_model = None
        
        # Initialize AI services
        if Config.USE_LLM:
            if Config.LLM_TYPE == "openai" and OPENAI_AVAILABLE and Config.OPENAI_API_KEY:
                openai.api_key = Config.OPENAI_API_KEY
                self.openai_client = openai.OpenAI()
            elif Config.LLM_TYPE == "gemini" and GEMINI_AVAILABLE and Config.GEMINI_API_KEY:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    def generate_response(self, query, system_context=""):
        # Simple responses without LLM
        if not Config.USE_LLM or (not self.openai_client and not self.gemini_model):
            return None
        
        # Get recent conversation history
        conversation_history = self.memory.memories["conversations"][-5:]
        conversation_context = ""
        for conv in conversation_history:
            conversation_context += f"User: {conv['user_input']}\nAssistant: {conv['assistant_response']}\n"
        
        # Create a complete prompt with system context and conversation history
        full_context = f"{system_context}\n\nConversation History:\n{conversation_context}\n\nUser: {query}\nAssistant:"
        
        try:
            if Config.LLM_TYPE == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_context},
                        {"role": "user", "content": query}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            
            elif Config.LLM_TYPE == "gemini" and self.gemini_model:
                response = self.gemini_model.generate_content(full_context)
                return response.text.strip()
            
            else:
                return None
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return None

# ====== Command Processor ======
class CommandProcessor:
    def __init__(self, speech_engine, system_controller, memory, intelligence):
        self.speech_engine = speech_engine
        self.system = system_controller
        self.memory = memory
        self.intelligence = intelligence
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
            "take screenshot": self._handle_screenshot,
            "system info": self._handle_system_info,
            "set volume": self._handle_volume,
            "set brightness": self._handle_brightness,
            "play": self._handle_play_pause,
            "pause": self._handle_play_pause,
            "next track": self._handle_next_track,
            "previous track": self._handle_previous_track,
            "lock computer": self._handle_lock_computer,
            "what time": self._handle_get_time,
            "what date": self._handle_get_date,
            "what day": self._handle_get_date,
            "switch window": self._handle_switch_window,
            "switch tab": self._handle_switch_tab,
            "undo": self._handle_undo
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
        # Extract the text to type after "type" or "write"
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
        # Extract search query after "search for" or "google"
        query = ""
        if "search for" in command:
            query = command.split("search for", 1)[1].strip()
        elif "google" in command:
            query = command.split("google", 1)[1].strip()
        
        if query:
            return self.system.search_web(query)
        else:
            return "What would you like me to search for?"
    
    def _handle_volume(self, command):
        if "up" in command:
            keyboard.press_and_release('volume up')
            return "Volume increased"
        elif "down" in command:
            keyboard.press_and_release('volume down')
            return "Volume decreased"
        elif "mute" in command:
            keyboard.press_and_release('volume mute')
            return "Audio muted"
        elif "unmute" in command:
            keyboard.press_and_release('volume mute')  # Toggle mute
            return "Audio unmuted"
        else:
            # Try to extract volume level
            try:
                import re
                numbers = re.findall(r'\d+', command)
                if numbers:
                    level = int(numbers[0])
                    if 0 <= level <= 100:
                        # Use a basic volume setting approach
                        current_vol = 50  # Assume current volume
                        if level > current_vol:
                            for _ in range((level - current_vol) // 2):
                                keyboard.press_and_release('volume up')
                        else:
                            for _ in range((current_vol - level) // 2):
                                keyboard.press_and_release('volume down')
                        return f"Volume set to approximately {level}%"
                    else:
                        return "Volume level should be between 0 and 100"
                else:
                    return "Please specify volume level or say 'volume up/down/mute'"
            except:
                return "Please specify a volume level between 0 and 100"
    
    def _handle_brightness(self, command):
        # Extract brightness level
        try:
            level = int(''.join(filter(str.isdigit, command)))
            return self.system.set_brightness(level)
        except:
            return "Please specify a brightness level between 0 and 100"
    
    def process_command(self, command):
        command_lower = command.lower().strip()
        
        # Check for custom commands
        custom_commands = self.memory.memories["custom_commands"]
        for cmd_name, action in custom_commands.items():
            if cmd_name.lower() in command_lower:
                return f"Executing custom command: {cmd_name}", action
        
        # Enhanced command matching with better logic
        # First check for exact phrase matches
        for key_phrase, handler in self.commands.items():
            if key_phrase.lower() in command_lower:
                try:
                    response = handler(command_lower)
                    return response, None
                except Exception as e:
                    return f"Error executing command: {e}", None
        
        # Additional command variations and aliases
        command_aliases = {
            "screenshot": "take screenshot",
            "screen shot": "take screenshot", 
            "screen capture": "take screenshot",
            "volume up": "set volume up",
            "volume down": "set volume down",
            "mute": "set volume mute",
            "unmute": "set volume unmute",
            "shutdown": "shutdown computer",
            "restart": "restart computer", 
            "sleep": "sleep computer",
            "time": "what time",
            "date": "what date",
            "day": "what day",
            "tell me a joke": "joke",
            "joke": "tell joke",
            "weather": "get weather",
            "system": "system info",
            "info": "system info"
        }
        
        # Check aliases
        for alias, actual_command in command_aliases.items():
            if alias in command_lower:
                if actual_command in self.commands:
                    try:
                        response = self.commands[actual_command](command_lower)
                        return response, None
                    except Exception as e:
                        return f"Error executing {actual_command}: {e}", None
                else:
                    # Handle special cases
                    if "joke" in actual_command:
                        return self._handle_joke(), None
                    elif "weather" in actual_command:
                        return self._handle_weather(), None
                    elif "volume" in actual_command:
                        return self._handle_volume(command_lower), None
                    elif "shutdown" in actual_command:
                        return self.system.shutdown_computer(), None
                    elif "restart" in actual_command:
                        return self.system.restart_computer(), None
                    elif "sleep" in actual_command:
                        return self.system.sleep_computer(), None
        
        # If no command matched, use AI
        system_context = """
        You are Vecna, an advanced AI assistant. You help with computer tasks and answer questions.
        Be concise, helpful, and a bit mysterious. Keep responses under 50 words when possible.
        """
        
        ai_response = self.intelligence.generate_response(command, system_context)
        if ai_response:
            return ai_response, None
        else:
            return "I'm not sure how to help with that. Could you rephrase your request?", None
    
    def _handle_joke(self):
        jokes = [
            "Why don't computers ever get cold? Because they have Windows!",
            "Why was the computer tired? It had a hard drive!",
            "What do you call a computer that sings? A Dell!",
            "Why don't programmers like nature? It has too many bugs!",
            "How does a computer get drunk? It takes screenshots!"
        ]
        import random
        return random.choice(jokes)
    
    def _handle_weather(self):
        return "I would need a weather API key to get current weather information. You can set this up in your configuration."
    
    # Wrapper functions for static methods to handle command parameter
    def _handle_screenshot(self, command):
        return self.system.take_screenshot()
    
    def _handle_system_info(self, command):
        return self.system.get_system_info()
    
    def _handle_play_pause(self, command):
        return self.system.play_pause_media()
    
    def _handle_next_track(self, command):
        return self.system.next_track()
    
    def _handle_previous_track(self, command):
        return self.system.previous_track()
    
    def _handle_lock_computer(self, command):
        return self.system.lock_computer()
    
    def _handle_get_time(self, command):
        return self.system.get_current_time()
    
    def _handle_get_date(self, command):
        return self.system.get_current_date()
    
    def _handle_switch_window(self, command):
        return self.system.switch_window()
    
    def _handle_switch_tab(self, command):
        return self.system.switch_tab()
    
    def _handle_undo(self, command):
        return self.system.undo()

# ====== Wake Word Detector ======
class WakeWordDetector:
    def __init__(self, recognizer, speech_engine):
        self.recognizer = recognizer
        self.speech_engine = speech_engine
        self.wake_words = Config.WAKE_WORDS
    
    def listen_for_wake_word(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening for wake word...")
                    self.recognizer.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.recognizer.listen(source, phrase_time_limit=3)
                
                try:
                    # Use Google Speech Recognition for wake word detection
                    text = self.recognizer.recognizer.recognize_google(audio).lower()
                    print(f"Potential wake word: {text}")
                    
                    for wake_word in self.wake_words:
                        if wake_word in text:
                            print(f"Wake word detected: {wake_word}")
                            return True
                
                except sr.UnknownValueError:
                    # Speech not understood, continue listening
                    pass
                except sr.RequestError:
                    print("Could not request results from Google Speech Recognition service")
                    # Switch to offline mode if network error
                    Config.OFFLINE_MODE = True
                    
            except Exception as e:
                print(f"Error in wake word detection: {e}")
                time.sleep(1)  # Add a delay to prevent CPU overuse in case of errors

# ====== Main Assistant Class ======
class VecnaAssistant:
    def __init__(self):
        # Initialize components
        self.memory = Memory()
        self.speech_engine = SpeechEngine()
        self.recognizer = SpeechRecognizer()
        self.system = SystemController()
        self.intelligence = Intelligence(self.memory)
        self.command_processor = CommandProcessor(self.speech_engine, self.system, self.memory, self.intelligence)
        
        # Check for pending reminders
        self._check_reminders()
    
    def _check_reminders(self):
        pending = self.memory.get_pending_reminders()
        if pending:
            self.speech_engine.speak(f"You have {len(pending)} pending reminders.")
            for reminder in pending:
                self.speech_engine.speak(reminder["text"])
    
    def _show_pyaudio_install_options(self):
        """Display multiple options for installing PyAudio"""
        print("\nAlternative PyAudio installation methods:")
        print("Option 1: Using pipwin (often works on Windows)")
        print("  pip install pipwin")
        print("  pipwin install pyaudio")
        print("\nOption 2: Using pre-built wheel")
        print("  1. Go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
        print("  2. Download the appropriate wheel file for your Python version")
        print("     (e.g., PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl for Python 3.10 64-bit)")
        print("  3. Install using: pip install path\\to\\downloaded\\wheel\\file.whl")
        print("\nOption 3: Using conda (if you have Anaconda/Miniconda)")
        print("  conda install -c anaconda pyaudio")
        print("\nOption 4: For development environments with Microsoft Visual C++")
        print("  pip install --upgrade setuptools")
        print("  pip install pyaudio")
    
    def startup(self):
        # Check if required packages are installed
        missing_packages = []
        
        # Check for PyAudio which is required by SpeechRecognition
        try:
            import pyaudio
        except ImportError:
            print("\n============== IMPORTANT NOTICE ==============")
            print("PyAudio is required for microphone access but is not installed.")
            print("Attempting to install PyAudio automatically...")
            
            # Try direct installation first
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "PyAudio"])
                print("Successfully installed PyAudio!")
                try:
                    import pyaudio
                    print("PyAudio imported successfully!")
                except ImportError:
                    self._show_pyaudio_install_options()
            except Exception as e:
                print(f"Failed to install PyAudio directly: {e}")
                self._show_pyaudio_install_options()
                
            print("==============================================\n")
            self.speech_engine.speak("PyAudio installation attempted. Check console for results.")
        
        try:
            import screen_brightness_control
        except ImportError:
            missing_packages.append("screen-brightness-control")
        
        try:
            import pygetwindow
        except ImportError:
            missing_packages.append("pygetwindow")
        
        try:
            import psutil
        except ImportError:
            missing_packages.append("psutil")
        
        try:
            import keyboard
        except ImportError:
            missing_packages.append("keyboard")
        
        if Config.USE_WHISPER and not WHISPER_AVAILABLE:
            missing_packages.append("faster-whisper")
        
        if Config.LLM_TYPE == "openai" and not OPENAI_AVAILABLE:
            missing_packages.append("openai")
        
        if Config.LLM_TYPE == "gemini" and not GEMINI_AVAILABLE:
            missing_packages.append("google-generativeai")
        
        # Install missing packages
        if missing_packages:
            self.speech_engine.speak(f"Installing {len(missing_packages)} required packages. This may take a moment.")
            for package in missing_packages:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    print(f"Installed {package}")
                except:
                    print(f"Failed to install {package}")
        
        # Startup message
        self.speech_engine.speak(f"Vecna initialized. At your command.")
    
    def run(self):
        self.startup()
        self.speech_engine.speak("Vecna is now listening continuously. No wake word needed.")
        
        while True:
            # Listen for command directly - no wake word needed
            print("🎤 Listening for command...")
            try:
                audio = self.recognizer.listen()
                command = self.recognizer.recognize(audio)
                
                if command:
                    print(f"You said: {command}")
                    
                    # Process the command
                    response, action = self.command_processor.process_command(command)
                    
                    # Save the interaction to memory
                    self.memory.add_conversation(command, response)
                    
                    # Speak the response
                    self.speech_engine.speak(response)
                    
                    # Execute any actions returned by the command processor
                    if action:
                        try:
                            exec(action)
                        except Exception as e:
                            print(f"Error executing action: {e}")
                # Don't say anything if no command was detected
            except Exception as e:
                print(f"Error listening for command: {e}")
                time.sleep(1)


# ====== Run Assistant ======
if __name__ == "__main__":
    vecna = VecnaAssistant()
    vecna.run()
