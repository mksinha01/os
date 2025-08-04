# import os
# import time
# import speech_recognition as sr
# import pyttsx3
# import pyautogui
# import pyperclip
# # ====== Text-to-Speech ======
# engine = pyttsx3.init()
# def speak(text):
#     print("Assistant:", text)
#     engine.say(text)
#     engine.runAndWait()

# # ====== Voice Recognition ======
# def take_command():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("🎤 Listening...")
#         recognizer.pause_threshold = 1
#         audio = recognizer.listen(source)
#     try:
#         print("🧠 Recognizing...")
#         query = recognizer.recognize_google(audio, language='en-in')
#         print("You:", query)
#         return query.lower()
#     except Exception:
#         speak("Sorry, please say that again.")
#         return ""

# # ====== Open App by Voice ======
# def open_app(app_name):
#     paths = {
#         "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
#         "notepad": "notepad",
#         "whatsapp": f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
#         "spotify": f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\Spotify\\Spotify.exe",
#         "brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
#         "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
#         "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
#         "vscode": f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
#         "paint": "mspaint",
#         "calculator": "calc",
#         "command prompt": "cmd",
#         "file explorer": "explorer"
#     }

#     matched = [key for key in paths if key in app_name]
#     if matched:
#         exe_path = paths[matched[0]]
#         try:
#             speak(f"Opening {matched[0]}")
#             os.startfile(os.path.expandvars(exe_path))
#         except FileNotFoundError:
#             speak(f"{matched[0]} not found on your system.")
#     else:
#         speak(f"{app_name} not found in app list.")

# # ====== Open Folder ======
# def open_folder(folder):
#     folders = {
#         "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
#         "documents": os.path.join(os.path.expanduser("~"), "Documents"),
#         "desktop": os.path.join(os.path.expanduser("~"), "Desktop")
#     }
#     if folder in folders:
#         speak(f"Opening {folder}")
#         os.startfile(folders[folder])

# # ====== Close Tab or App ======
# def close_tab():
#     pyautogui.hotkey("ctrl", "w")
#     speak("Closed the current tab or window.")

# # ====== Main Loop ======
# def main():
#     speak("Voice Assistant activated. Waiting for your command.")

#     while True:
#         command = take_command()

#         if not command:
#             continue

#         # === App Control ===
#         elif "open" in command:
#             open_app(command)
#             for folder in ["downloads", "documents", "desktop"]:
#                 if folder in command:
#                     open_folder(folder)

#         # === Close Tab ===
#         elif "close tab" in command or "close window" in command:
#             close_tab()

#         # === Write something ===
#         elif "write" in command:
#             speak("What should I write?")
#             text = take_command()
#             pyautogui.write(text)
#             speak("Done writing.")

#         # === Read something ===
#         elif "read" in command:
#             speak("Reading...")
#             pyautogui.hotkey("ctrl", "a")
#             time.sleep(0.5)
#             pyautogui.hotkey("ctrl", "c")
#             time.sleep(0.5)
#             text = pyperclip.paste()
#             speak(text)

#         # === Exit ===
#         elif "exit" in command or "stop" in command:
#             speak("Goodbye!")
#             break

#         else:
#             speak("Command not recognized.")

# if __name__ == "__main__":
#     main()
