import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import sys
import os
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item
import queue
import time

class VecnaGUI:
    def __init__(self, vecna_assistant):
        self.vecna = vecna_assistant
        self.root = tk.Tk()
        self.root.title("Vecna Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Message queue for thread-safe GUI updates
        self.message_queue = queue.Queue()
        
        self.setup_gui()
        self.setup_system_tray()
        
        # Start checking for messages
        self.check_messages()
        
    def setup_gui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="VECNA", font=("Arial", 24, "bold"), 
                              fg='#ff6b6b', bg='#1a1a1a')
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = tk.Label(status_frame, text="🎤 Listening...", 
                                    font=("Arial", 12), fg='#4ecdc4', bg='#2d2d2d')
        self.status_label.pack(pady=10)
        
        # Conversation area
        conv_frame = tk.LabelFrame(main_frame, text="Conversation", font=("Arial", 12, "bold"),
                                  fg='#ffffff', bg='#1a1a1a')
        conv_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.conversation_text = scrolledtext.ScrolledText(conv_frame, height=15, width=70,
                                                          bg='#2d2d2d', fg='#ffffff',
                                                          font=("Consolas", 10))
        self.conversation_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(fill=tk.X)
        
        self.toggle_btn = tk.Button(button_frame, text="Pause Listening", 
                                   command=self.toggle_listening,
                                   bg='#ff6b6b', fg='white', font=("Arial", 10, "bold"))
        self.toggle_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(button_frame, text="Clear Chat", 
                             command=self.clear_conversation,
                             bg='#4ecdc4', fg='white', font=("Arial", 10, "bold"))
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        settings_btn = tk.Button(button_frame, text="Settings", 
                               command=self.open_settings,
                               bg='#45b7d1', fg='white', font=("Arial", 10, "bold"))
        settings_btn.pack(side=tk.LEFT)
        
        # Minimize to tray instead of closing
        self.root.protocol("WM_DELETE_WINDOW", self.hide_to_tray)
        
    def setup_system_tray(self):
        # Create system tray icon
        try:
            # Create a simple icon (you can replace with a proper .ico file)
            image = Image.new('RGB', (64, 64), color='red')
            
            menu = pystray.Menu(
                item('Show', self.show_from_tray),
                item('Pause/Resume', self.toggle_listening),
                item('Exit', self.quit_app)
            )
            
            self.tray_icon = pystray.Icon("Vecna", image, "Vecna Voice Assistant", menu)
        except Exception as e:
            print(f"Could not create system tray icon: {e}")
            self.tray_icon = None
    
    def hide_to_tray(self):
        self.root.withdraw()
        if self.tray_icon:
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
    
    def show_from_tray(self):
        self.root.deiconify()
        self.root.lift()
        if self.tray_icon:
            self.tray_icon.stop()
    
    def quit_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
        sys.exit()
    
    def toggle_listening(self):
        # This would connect to your Vecna assistant's pause/resume functionality
        # You'll need to implement pause/resume in the main Vecna class
        pass
    
    def clear_conversation(self):
        self.conversation_text.delete(1.0, tk.END)
    
    def open_settings(self):
        # Open settings window
        SettingsWindow(self.root, self.vecna)
    
    def add_message(self, speaker, message, timestamp=None):
        """Thread-safe method to add messages to conversation"""
        if timestamp is None:
            timestamp = time.strftime("%H:%M:%S")
        
        self.message_queue.put(('message', speaker, message, timestamp))
    
    def update_status(self, status):
        """Thread-safe method to update status"""
        self.message_queue.put(('status', status))
    
    def check_messages(self):
        """Check for queued messages and update GUI"""
        try:
            while True:
                msg_type, *data = self.message_queue.get_nowait()
                
                if msg_type == 'message':
                    speaker, message, timestamp = data
                    color = '#4ecdc4' if speaker == 'You' else '#ff6b6b'
                    
                    self.conversation_text.insert(tk.END, f"[{timestamp}] {speaker}: {message}\n")
                    self.conversation_text.tag_add(speaker, "end-2l linestart", "end-2l lineend")
                    self.conversation_text.tag_config(speaker, foreground=color)
                    self.conversation_text.see(tk.END)
                
                elif msg_type == 'status':
                    status = data[0]
                    self.status_label.config(text=status)
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_messages)
    
    def run(self):
        self.root.mainloop()

class SettingsWindow:
    def __init__(self, parent, vecna_assistant):
        self.vecna = vecna_assistant
        self.window = tk.Toplevel(parent)
        self.window.title("Vecna Settings")
        self.window.geometry("500x400")
        self.window.configure(bg='#1a1a1a')
        
        self.setup_settings_gui()
    
    def setup_settings_gui(self):
        # Notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Voice settings tab
        voice_frame = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(voice_frame, text="Voice")
        
        # Voice rate
        tk.Label(voice_frame, text="Voice Rate:", fg='white', bg='#1a1a1a').pack(anchor='w', pady=5)
        self.rate_var = tk.IntVar(value=180)
        rate_scale = tk.Scale(voice_frame, from_=50, to=300, orient=tk.HORIZONTAL, 
                             variable=self.rate_var, bg='#2d2d2d', fg='white')
        rate_scale.pack(fill=tk.X, pady=5)
        
        # Voice volume
        tk.Label(voice_frame, text="Voice Volume:", fg='white', bg='#1a1a1a').pack(anchor='w', pady=5)
        self.volume_var = tk.DoubleVar(value=1.0)
        volume_scale = tk.Scale(voice_frame, from_=0.0, to=1.0, resolution=0.1,
                               orient=tk.HORIZONTAL, variable=self.volume_var, 
                               bg='#2d2d2d', fg='white')
        volume_scale.pack(fill=tk.X, pady=5)
        
        # Recognition settings tab
        recognition_frame = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(recognition_frame, text="Recognition")
        
        # Whisper model selection
        tk.Label(recognition_frame, text="Whisper Model:", fg='white', bg='#1a1a1a').pack(anchor='w', pady=5)
        self.model_var = tk.StringVar(value="base")
        model_combo = ttk.Combobox(recognition_frame, textvariable=self.model_var,
                                  values=["tiny", "base", "small", "medium", "large"])
        model_combo.pack(fill=tk.X, pady=5)
        
        # AI settings tab
        ai_frame = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(ai_frame, text="AI")
        
        # API keys
        tk.Label(ai_frame, text="OpenAI API Key:", fg='white', bg='#1a1a1a').pack(anchor='w', pady=5)
        self.openai_key = tk.Entry(ai_frame, show="*", bg='#2d2d2d', fg='white')
        self.openai_key.pack(fill=tk.X, pady=5)
        
        tk.Label(ai_frame, text="Gemini API Key:", fg='white', bg='#1a1a1a').pack(anchor='w', pady=5)
        self.gemini_key = tk.Entry(ai_frame, show="*", bg='#2d2d2d', fg='white')
        self.gemini_key.pack(fill=tk.X, pady=5)
        
        # Save button
        save_btn = tk.Button(self.window, text="Save Settings", command=self.save_settings,
                           bg='#4ecdc4', fg='white', font=("Arial", 10, "bold"))
        save_btn.pack(pady=20)
    
    def save_settings(self):
        # Save settings to config
        # You'll need to implement this in your main Vecna class
        self.window.destroy()

# Example of how to integrate with your existing Vecna class
if __name__ == "__main__":
    # You would import and initialize your VecnaAssistant here
    # vecna = VecnaAssistant()
    # gui = VecnaGUI(vecna)
    # gui.run()
    
    # For now, create a dummy GUI
    root = tk.Tk()
    gui = VecnaGUI(None)
    gui.run()
