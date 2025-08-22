"""
Vecna Control Panel - Futuristic Desktop Interface
A transparent, robotic-themed control window for managing all Vecna features
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import psutil
import datetime
import os
import sys

# Add the current directory to path to import vecna modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from vecna import VecnaAssistant, Config
    VECNA_AVAILABLE = True
except ImportError:
    VECNA_AVAILABLE = False
    print("Vecna modules not found - running in demo mode")

class FuturisticVecnaControlPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_interface()
        self.vecna_instance = None
        self.is_listening = False
        self.system_monitor_active = True
        
        # Start system monitoring
        self.start_system_monitoring()
        
    def setup_window(self):
        """Configure the main window with futuristic styling"""
        self.root.title("🤖 Vecna Control Panel")
        self.root.geometry("1200x800")
        
        # Make window transparent and modern
        self.root.configure(bg='#0a0a0a')
        self.root.attributes('-alpha', 0.95)  # Slight transparency
        
        # Remove default window decorations for futuristic look
        self.root.overrideredirect(False)  # Keep window controls for now
        
        # Make window always on top (optional)
        # self.root.attributes('-topmost', True)
        
        # Center window on screen
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
    def setup_styles(self):
        """Configure custom styles for futuristic look"""
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_panel': '#1a1a2e',
            'accent_cyan': '#00fff5',
            'accent_purple': '#8a2be2',
            'accent_green': '#00ff00',
            'accent_orange': '#ff6b00',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'border': '#333333'
        }
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom button style
        style.configure('Cyber.TButton',
                       background='#1a1a2e',
                       foreground='#00fff5',
                       borderwidth=1,
                       focuscolor='none',
                       relief='flat')
        
        style.map('Cyber.TButton',
                 background=[('active', '#2a2a3e'),
                           ('pressed', '#0a0a1e')])
        
    def create_interface(self):
        """Create the main interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_frame)
        
        # Create notebook for different sections
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Create tabs
        self.create_voice_control_tab()
        self.create_system_monitor_tab()
        self.create_features_tab()
        self.create_plugins_tab()
        self.create_settings_tab()
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        """Create the header with title and main controls"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_dark'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="🤖 VECNA CONTROL PANEL", 
                              font=('Orbitron', 24, 'bold'),
                              fg=self.colors['accent_cyan'],
                              bg=self.colors['bg_dark'])
        title_label.pack(side=tk.LEFT, pady=20)
        
        # Main control buttons
        controls_frame = tk.Frame(header_frame, bg=self.colors['bg_dark'])
        controls_frame.pack(side=tk.RIGHT, pady=20)
        
        self.start_btn = tk.Button(controls_frame, 
                                  text="🚀 START VECNA",
                                  font=('Orbitron', 12, 'bold'),
                                  bg=self.colors['accent_green'],
                                  fg='black',
                                  relief='flat',
                                  padx=20, pady=10,
                                  command=self.start_vecna)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(controls_frame,
                                 text="⏹️ STOP VECNA",
                                 font=('Orbitron', 12, 'bold'),
                                 bg=self.colors['accent_orange'],
                                 fg='black',
                                 relief='flat',
                                 padx=20, pady=10,
                                 command=self.stop_vecna,
                                 state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
    def create_voice_control_tab(self):
        """Create voice control and conversation tab"""
        voice_frame = tk.Frame(self.notebook, bg=self.colors['bg_dark'])
        self.notebook.add(voice_frame, text="🎤 Voice Control")
        
        # Split into two sections
        left_frame = tk.Frame(voice_frame, bg=self.colors['bg_panel'], relief='ridge', bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_frame = tk.Frame(voice_frame, bg=self.colors['bg_panel'], relief='ridge', bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Voice status section
        status_label = tk.Label(left_frame, 
                               text="🎙️ VOICE STATUS", 
                               font=('Orbitron', 14, 'bold'),
                               fg=self.colors['accent_cyan'],
                               bg=self.colors['bg_panel'])
        status_label.pack(pady=10)
        
        self.voice_status = tk.Label(left_frame,
                                    text="⚫ OFFLINE",
                                    font=('Rajdhani', 12),
                                    fg=self.colors['accent_orange'],
                                    bg=self.colors['bg_panel'])
        self.voice_status.pack(pady=5)
        
        # Microphone level indicator
        mic_frame = tk.Frame(left_frame, bg=self.colors['bg_panel'])
        mic_frame.pack(pady=20)
        
        tk.Label(mic_frame, text="MIC LEVEL:", 
                font=('Rajdhani', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_panel']).pack()
        
        self.mic_canvas = tk.Canvas(mic_frame, width=200, height=20, 
                                   bg=self.colors['bg_dark'], highlightthickness=0)
        self.mic_canvas.pack(pady=5)
        
        # Voice commands section
        commands_label = tk.Label(left_frame,
                                 text="📋 QUICK COMMANDS",
                                 font=('Orbitron', 12, 'bold'),
                                 fg=self.colors['accent_purple'],
                                 bg=self.colors['bg_panel'])
        commands_label.pack(pady=(20, 10))
        
        commands = [
            ("📸 Take Screenshot", "screenshot"),
            ("🕒 What Time", "what time is it"),
            ("💻 System Info", "system info"),
            ("🎵 Volume Up", "volume up"),
            ("🎵 Volume Down", "volume down"),
            ("😄 Tell Joke", "tell me a joke"),
            ("🌐 Open Chrome", "open chrome"),
            ("📝 Open Notepad", "open notepad")
        ]
        
        for cmd_text, cmd_voice in commands:
            btn = tk.Button(left_frame,
                           text=cmd_text,
                           font=('Rajdhani', 10),
                           bg=self.colors['bg_dark'],
                           fg=self.colors['text_primary'],
                           relief='flat',
                           padx=10, pady=5,
                           command=lambda cmd=cmd_voice: self.execute_voice_command(cmd))
            btn.pack(fill=tk.X, padx=10, pady=2)
        
        # Conversation history
        history_label = tk.Label(right_frame,
                                text="💬 CONVERSATION HISTORY",
                                font=('Orbitron', 14, 'bold'),
                                fg=self.colors['accent_cyan'],
                                bg=self.colors['bg_panel'])
        history_label.pack(pady=10)
        
        # Text area for conversation
        conv_frame = tk.Frame(right_frame, bg=self.colors['bg_panel'])
        conv_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.conversation_text = tk.Text(conv_frame,
                                        bg=self.colors['bg_dark'],
                                        fg=self.colors['text_primary'],
                                        font=('Courier New', 10),
                                        relief='flat',
                                        wrap=tk.WORD)
        
        conv_scrollbar = tk.Scrollbar(conv_frame, orient=tk.VERTICAL, command=self.conversation_text.yview)
        self.conversation_text.configure(yscrollcommand=conv_scrollbar.set)
        
        self.conversation_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        conv_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add initial welcome message
        self.add_conversation_message("SYSTEM", "Vecna Control Panel initialized. Ready for voice commands.")
        
    def create_system_monitor_tab(self):
        """Create system monitoring tab"""
        system_frame = tk.Frame(self.notebook, bg=self.colors['bg_dark'])
        self.notebook.add(system_frame, text="📊 System Monitor")
        
        # System stats grid
        stats_frame = tk.Frame(system_frame, bg=self.colors['bg_dark'])
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # CPU Section
        cpu_frame = tk.Frame(stats_frame, bg=self.colors['bg_panel'], relief='ridge', bd=2)
        cpu_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        tk.Label(cpu_frame, text="🔥 CPU USAGE", 
                font=('Orbitron', 12, 'bold'),
                fg=self.colors['accent_green'],
                bg=self.colors['bg_panel']).pack(pady=5)
        
        self.cpu_label = tk.Label(cpu_frame, text="0%", 
                                 font=('Rajdhani', 20, 'bold'),
                                 fg=self.colors['text_primary'],
                                 bg=self.colors['bg_panel'])
        self.cpu_label.pack(pady=5)
        
        # RAM Section
        ram_frame = tk.Frame(stats_frame, bg=self.colors['bg_panel'], relief='ridge', bd=2)
        ram_frame.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Label(ram_frame, text="🧠 RAM USAGE",
                font=('Orbitron', 12, 'bold'),
                fg=self.colors['accent_cyan'],
                bg=self.colors['bg_panel']).pack(pady=5)
        
        self.ram_label = tk.Label(ram_frame, text="0%",
                                 font=('Rajdhani', 20, 'bold'),
                                 fg=self.colors['text_primary'],
                                 bg=self.colors['bg_panel'])
        self.ram_label.pack(pady=5)
        
        # Disk Section
        disk_frame = tk.Frame(stats_frame, bg=self.colors['bg_panel'], relief='ridge', bd=2)
        disk_frame.grid(row=0, column=2, padx=5, pady=5, sticky='ew')
        
        tk.Label(disk_frame, text="💾 DISK USAGE",
                font=('Orbitron', 12, 'bold'),
                fg=self.colors['accent_purple'],
                bg=self.colors['bg_panel']).pack(pady=5)
        
        self.disk_label = tk.Label(disk_frame, text="0%",
                                  font=('Rajdhani', 20, 'bold'),
                                  fg=self.colors['text_primary'],
                                  bg=self.colors['bg_panel'])
        self.disk_label.pack(pady=5)
        
        # Battery Section
        battery_frame = tk.Frame(stats_frame, bg=self.colors['bg_panel'], relief='ridge', bd=2)
        battery_frame.grid(row=0, column=3, padx=5, pady=5, sticky='ew')
        
        tk.Label(battery_frame, text="🔋 BATTERY",
                font=('Orbitron', 12, 'bold'),
                fg=self.colors['accent_orange'],
                bg=self.colors['bg_panel']).pack(pady=5)
        
        self.battery_label = tk.Label(battery_frame, text="N/A",
                                     font=('Rajdhani', 20, 'bold'),
                                     fg=self.colors['text_primary'],
                                     bg=self.colors['bg_panel'])
        self.battery_label.pack(pady=5)
        
        # Configure grid weights
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)
        stats_frame.grid_columnconfigure(3, weight=1)
        
        # Process list
        process_frame = tk.Frame(system_frame, bg=self.colors['bg_panel'], relief='ridge', bd=2)
        process_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(process_frame, text="⚙️ RUNNING PROCESSES",
                font=('Orbitron', 14, 'bold'),
                fg=self.colors['accent_cyan'],
                bg=self.colors['bg_panel']).pack(pady=10)
        
        # Treeview for processes
        process_tree_frame = tk.Frame(process_frame, bg=self.colors['bg_panel'])
        process_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('PID', 'Name', 'CPU%', 'Memory%')
        self.process_tree = ttk.Treeview(process_tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100)
        
        process_scrollbar = ttk.Scrollbar(process_tree_frame, orient=tk.VERTICAL, command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=process_scrollbar.set)
        
        self.process_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        process_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Process control buttons
        process_controls = tk.Frame(process_frame, bg=self.colors['bg_panel'])
        process_controls.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(process_controls, text="🔄 Refresh",
                 font=('Rajdhani', 10),
                 bg=self.colors['accent_cyan'],
                 fg='black',
                 relief='flat',
                 command=self.refresh_processes).pack(side=tk.LEFT, padx=5)
        
        tk.Button(process_controls, text="❌ Kill Process",
                 font=('Rajdhani', 10),
                 bg=self.colors['accent_orange'],
                 fg='black',
                 relief='flat',
                 command=self.kill_selected_process).pack(side=tk.LEFT, padx=5)
        
    def create_features_tab(self):
        """Create features control tab"""
        features_frame = tk.Frame(self.notebook, bg=self.colors['bg_dark'])
        self.notebook.add(features_frame, text="🎯 Features")
        
        # Features grid
        features_grid = tk.Frame(features_frame, bg=self.colors['bg_dark'])
        features_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        feature_categories = [
            {
                'title': '🎤 Voice Control',
                'color': self.colors['accent_cyan'],
                'features': [
                    ('Start Listening', self.start_listening),
                    ('Stop Listening', self.stop_listening),
                    ('Voice Settings', self.voice_settings),
                    ('Microphone Test', self.test_microphone)
                ]
            },
            {
                'title': '💻 System Control',
                'color': self.colors['accent_green'],
                'features': [
                    ('Take Screenshot', lambda: self.execute_voice_command('screenshot')),
                    ('Lock Computer', lambda: self.execute_voice_command('lock computer')),
                    ('Volume Control', self.volume_control),
                    ('Power Options', self.power_options)
                ]
            },
            {
                'title': '🤖 AI Features',
                'color': self.colors['accent_purple'],
                'features': [
                    ('Chat with AI', self.ai_chat),
                    ('Memory Manager', self.memory_manager),
                    ('AI Settings', self.ai_settings),
                    ('Clear History', self.clear_history)
                ]
            },
            {
                'title': '🔧 Advanced',
                'color': self.colors['accent_orange'],
                'features': [
                    ('Plugin Manager', self.plugin_manager),
                    ('Timer Control', self.timer_control),
                    ('File Operations', self.file_operations),
                    ('Network Monitor', self.network_monitor)
                ]
            }
        ]
        
        for i, category in enumerate(feature_categories):
            frame = tk.Frame(features_grid, bg=self.colors['bg_panel'], relief='ridge', bd=2)
            frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            
            # Category title
            title_label = tk.Label(frame, 
                                  text=category['title'],
                                  font=('Orbitron', 14, 'bold'),
                                  fg=category['color'],
                                  bg=self.colors['bg_panel'])
            title_label.pack(pady=10)
            
            # Feature buttons
            for feature_name, feature_func in category['features']:
                btn = tk.Button(frame,
                               text=feature_name,
                               font=('Rajdhani', 11),
                               bg=self.colors['bg_dark'],
                               fg=self.colors['text_primary'],
                               relief='flat',
                               padx=15, pady=8,
                               command=feature_func)
                btn.pack(fill=tk.X, padx=10, pady=3)
        
        # Configure grid weights
        features_grid.grid_rowconfigure(0, weight=1)
        features_grid.grid_rowconfigure(1, weight=1)
        features_grid.grid_columnconfigure(0, weight=1)
        features_grid.grid_columnconfigure(1, weight=1)
        
    def create_plugins_tab(self):
        """Create plugins management tab"""
        plugins_frame = tk.Frame(self.notebook, bg=self.colors['bg_dark'])
        self.notebook.add(plugins_frame, text="🧩 Plugins")
        
        # Plugins list
        plugins_list_frame = tk.Frame(plugins_frame, bg=self.colors['bg_panel'], relief='ridge', bd=2)
        plugins_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(plugins_list_frame, text="🧩 AVAILABLE PLUGINS",
                font=('Orbitron', 14, 'bold'),
                fg=self.colors['accent_cyan'],
                bg=self.colors['bg_panel']).pack(pady=10)
        
        # Plugin examples
        plugin_examples = [
            {'name': 'Weather Plugin', 'status': 'Enabled', 'desc': 'Get weather information'},
            {'name': 'Calculator Plugin', 'status': 'Enabled', 'desc': 'Perform calculations'},
            {'name': 'Todo Plugin', 'status': 'Enabled', 'desc': 'Manage tasks and reminders'},
            {'name': 'Music Plugin', 'status': 'Disabled', 'desc': 'Control music playback'},
            {'name': 'Email Plugin', 'status': 'Disabled', 'desc': 'Send and read emails'},
        ]
        
        plugins_scroll_frame = tk.Frame(plugins_list_frame, bg=self.colors['bg_panel'])
        plugins_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for plugin in plugin_examples:
            plugin_frame = tk.Frame(plugins_scroll_frame, bg=self.colors['bg_dark'], relief='ridge', bd=1)
            plugin_frame.pack(fill=tk.X, pady=5)
            
            # Plugin info
            info_frame = tk.Frame(plugin_frame, bg=self.colors['bg_dark'])
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            name_label = tk.Label(info_frame, text=plugin['name'],
                                 font=('Orbitron', 12, 'bold'),
                                 fg=self.colors['accent_cyan'],
                                 bg=self.colors['bg_dark'])
            name_label.pack(anchor='w')
            
            desc_label = tk.Label(info_frame, text=plugin['desc'],
                                 font=('Rajdhani', 10),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_dark'])
            desc_label.pack(anchor='w')
            
            # Plugin controls
            controls_frame = tk.Frame(plugin_frame, bg=self.colors['bg_dark'])
            controls_frame.pack(side=tk.RIGHT, padx=10, pady=10)
            
            status_color = self.colors['accent_green'] if plugin['status'] == 'Enabled' else self.colors['accent_orange']
            status_label = tk.Label(controls_frame, text=plugin['status'],
                                   font=('Rajdhani', 10, 'bold'),
                                   fg=status_color,
                                   bg=self.colors['bg_dark'])
            status_label.pack()
            
            toggle_btn = tk.Button(controls_frame,
                                  text="Toggle",
                                  font=('Rajdhani', 9),
                                  bg=self.colors['accent_purple'],
                                  fg='black',
                                  relief='flat',
                                  command=lambda p=plugin: self.toggle_plugin(p))
            toggle_btn.pack(pady=2)
        
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = tk.Frame(self.notebook, bg=self.colors['bg_dark'])
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings sections
        settings_scroll = tk.Frame(settings_frame, bg=self.colors['bg_dark'])
        settings_scroll.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Voice Settings
        voice_settings_frame = tk.Frame(settings_scroll, bg=self.colors['bg_panel'], relief='ridge', bd=2)
        voice_settings_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(voice_settings_frame, text="🎤 VOICE SETTINGS",
                font=('Orbitron', 12, 'bold'),
                fg=self.colors['accent_cyan'],
                bg=self.colors['bg_panel']).pack(pady=10)
        
        # Voice settings controls
        voice_controls_frame = tk.Frame(voice_settings_frame, bg=self.colors['bg_panel'])
        voice_controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Recognition engine
        tk.Label(voice_controls_frame, text="Recognition Engine:",
                font=('Rajdhani', 11),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_panel']).grid(row=0, column=0, sticky='w', pady=5)
        
        self.recognition_var = tk.StringVar(value="Google Speech API")
        recognition_combo = ttk.Combobox(voice_controls_frame, textvariable=self.recognition_var,
                                        values=["Google Speech API", "Whisper AI", "Both"],
                                        state="readonly")
        recognition_combo.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        
        # Sensitivity
        tk.Label(voice_controls_frame, text="Microphone Sensitivity:",
                font=('Rajdhani', 11),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_panel']).grid(row=1, column=0, sticky='w', pady=5)
        
        self.sensitivity_var = tk.IntVar(value=75)
        sensitivity_scale = tk.Scale(voice_controls_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                    variable=self.sensitivity_var,
                                    bg=self.colors['bg_panel'],
                                    fg=self.colors['accent_cyan'],
                                    highlightthickness=0)
        sensitivity_scale.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        
        voice_controls_frame.grid_columnconfigure(1, weight=1)
        
        # AI Settings
        ai_settings_frame = tk.Frame(settings_scroll, bg=self.colors['bg_panel'], relief='ridge', bd=2)
        ai_settings_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(ai_settings_frame, text="🤖 AI SETTINGS",
                font=('Orbitron', 12, 'bold'),
                fg=self.colors['accent_purple'],
                bg=self.colors['bg_panel']).pack(pady=10)
        
        # AI controls
        ai_controls_frame = tk.Frame(ai_settings_frame, bg=self.colors['bg_panel'])
        ai_controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # AI Provider
        tk.Label(ai_controls_frame, text="AI Provider:",
                font=('Rajdhani', 11),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_panel']).grid(row=0, column=0, sticky='w', pady=5)
        
        self.ai_provider_var = tk.StringVar(value="OpenAI GPT")
        ai_combo = ttk.Combobox(ai_controls_frame, textvariable=self.ai_provider_var,
                               values=["OpenAI GPT", "Google Gemini", "Local AI"],
                               state="readonly")
        ai_combo.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        
        ai_controls_frame.grid_columnconfigure(1, weight=1)
        
        # System Settings
        system_settings_frame = tk.Frame(settings_scroll, bg=self.colors['bg_panel'], relief='ridge', bd=2)
        system_settings_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(system_settings_frame, text="💻 SYSTEM SETTINGS",
                font=('Orbitron', 12, 'bold'),
                fg=self.colors['accent_green'],
                bg=self.colors['bg_panel']).pack(pady=10)
        
        # System controls
        system_controls_frame = tk.Frame(system_settings_frame, bg=self.colors['bg_panel'])
        system_controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Checkboxes for various settings
        self.startup_var = tk.BooleanVar(value=False)
        startup_check = tk.Checkbutton(system_controls_frame, text="Start with Windows",
                                      variable=self.startup_var,
                                      bg=self.colors['bg_panel'],
                                      fg=self.colors['text_primary'],
                                      selectcolor=self.colors['bg_dark'],
                                      activebackground=self.colors['bg_panel'])
        startup_check.pack(anchor='w', pady=2)
        
        self.notifications_var = tk.BooleanVar(value=True)
        notifications_check = tk.Checkbutton(system_controls_frame, text="Show notifications",
                                            variable=self.notifications_var,
                                            bg=self.colors['bg_panel'],
                                            fg=self.colors['text_primary'],
                                            selectcolor=self.colors['bg_dark'],
                                            activebackground=self.colors['bg_panel'])
        notifications_check.pack(anchor='w', pady=2)
        
        self.minimize_tray_var = tk.BooleanVar(value=True)
        tray_check = tk.Checkbutton(system_controls_frame, text="Minimize to system tray",
                                   variable=self.minimize_tray_var,
                                   bg=self.colors['bg_panel'],
                                   fg=self.colors['text_primary'],
                                   selectcolor=self.colors['bg_dark'],
                                   activebackground=self.colors['bg_panel'])
        tray_check.pack(anchor='w', pady=2)
        
        # Save settings button
        save_btn = tk.Button(settings_scroll,
                            text="💾 SAVE SETTINGS",
                            font=('Orbitron', 12, 'bold'),
                            bg=self.colors['accent_cyan'],
                            fg='black',
                            relief='flat',
                            padx=20, pady=10,
                            command=self.save_settings)
        save_btn.pack(pady=20)
        
    def create_status_bar(self, parent):
        """Create status bar at bottom"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_panel'], relief='sunken', bd=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(status_frame,
                                    text="🤖 Vecna Control Panel Ready • System Online",
                                    font=('Rajdhani', 10),
                                    fg=self.colors['accent_cyan'],
                                    bg=self.colors['bg_panel'])
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Time display
        self.time_label = tk.Label(status_frame,
                                  text="",
                                  font=('Rajdhani', 10),
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg_panel'])
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.update_time()
        
    def update_time(self):
        """Update time display"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def start_system_monitoring(self):
        """Start system monitoring thread"""
        def monitor():
            while self.system_monitor_active:
                try:
                    # Update system stats
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')
                    
                    # Update labels in main thread
                    self.root.after(0, lambda: self.cpu_label.config(text=f"{cpu_percent:.1f}%"))
                    self.root.after(0, lambda: self.ram_label.config(text=f"{memory.percent:.1f}%"))
                    self.root.after(0, lambda: self.disk_label.config(text=f"{disk.percent:.1f}%"))
                    
                    # Battery info
                    try:
                        battery = psutil.sensors_battery()
                        if battery:
                            self.root.after(0, lambda: self.battery_label.config(text=f"{battery.percent:.0f}%"))
                        else:
                            self.root.after(0, lambda: self.battery_label.config(text="N/A"))
                    except:
                        self.root.after(0, lambda: self.battery_label.config(text="N/A"))
                    
                    # Update processes
                    self.update_processes()
                    
                except Exception as e:
                    print(f"Monitoring error: {e}")
                
                time.sleep(2)
        
        threading.Thread(target=monitor, daemon=True).start()
        
    def update_processes(self):
        """Update process list"""
        try:
            # Clear existing items
            for item in self.process_tree.get_children():
                self.process_tree.delete(item)
            
            # Get top processes by CPU usage
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            # Sort by CPU usage and get top 10
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            top_processes = processes[:10]
            
            # Add to treeview
            for proc in top_processes:
                self.process_tree.insert('', 'end', values=(
                    proc['pid'],
                    proc['name'][:20] if proc['name'] else 'N/A',
                    f"{proc['cpu_percent']:.1f}" if proc['cpu_percent'] else '0.0',
                    f"{proc['memory_percent']:.1f}" if proc['memory_percent'] else '0.0'
                ))
        except Exception as e:
            print(f"Process update error: {e}")
    
    # Event handlers and methods
    def start_vecna(self):
        """Start Vecna assistant"""
        try:
            if VECNA_AVAILABLE and not self.is_listening:
                self.add_conversation_message("SYSTEM", "Starting Vecna voice assistant...")
                # Here you would start the actual Vecna instance
                # self.vecna_instance = VecnaAssistant()
                self.is_listening = True
                self.voice_status.config(text="🟢 ONLINE", fg=self.colors['accent_green'])
                self.start_btn.config(state='disabled')
                self.stop_btn.config(state='normal')
                self.status_label.config(text="🤖 Vecna Online • Listening for commands")
            else:
                self.add_conversation_message("SYSTEM", "Vecna modules not available - running in demo mode")
                self.voice_status.config(text="🟡 DEMO MODE", fg=self.colors['accent_orange'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Vecna: {e}")
    
    def stop_vecna(self):
        """Stop Vecna assistant"""
        if self.is_listening:
            self.add_conversation_message("SYSTEM", "Stopping Vecna voice assistant...")
            self.is_listening = False
            self.voice_status.config(text="⚫ OFFLINE", fg=self.colors['accent_orange'])
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.status_label.config(text="🤖 Vecna Offline • Ready to start")
    
    def execute_voice_command(self, command):
        """Execute a voice command"""
        self.add_conversation_message("USER", command)
        
        # Simulate command execution
        responses = {
            "screenshot": "Screenshot taken and saved to Pictures folder",
            "what time is it": f"Current time is {datetime.datetime.now().strftime('%H:%M:%S')}",
            "system info": f"CPU: {psutil.cpu_percent()}%, RAM: {psutil.virtual_memory().percent}%",
            "volume up": "Volume increased",
            "volume down": "Volume decreased",
            "tell me a joke": "Why don't computers catch cold? Because they have Windows!",
            "open chrome": "Launching Google Chrome",
            "open notepad": "Opening Notepad",
            "lock computer": "Computer will be locked"
        }
        
        response = responses.get(command, "Command executed")
        self.add_conversation_message("VECNA", response)
    
    def add_conversation_message(self, sender, message):
        """Add message to conversation history"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {sender}: {message}\n"
        
        self.conversation_text.insert(tk.END, formatted_message)
        self.conversation_text.see(tk.END)
    
    def refresh_processes(self):
        """Refresh process list"""
        self.update_processes()
    
    def kill_selected_process(self):
        """Kill selected process"""
        selection = self.process_tree.selection()
        if selection:
            item = self.process_tree.item(selection[0])
            pid = int(item['values'][0])
            name = item['values'][1]
            
            if messagebox.askyesno("Confirm", f"Kill process '{name}' (PID: {pid})?"):
                try:
                    proc = psutil.Process(pid)
                    proc.terminate()
                    self.add_conversation_message("SYSTEM", f"Process '{name}' terminated")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to kill process: {e}")
    
    # Feature functions (placeholders)
    def start_listening(self):
        self.add_conversation_message("SYSTEM", "Voice listening started")
    
    def stop_listening(self):
        self.add_conversation_message("SYSTEM", "Voice listening stopped")
    
    def voice_settings(self):
        messagebox.showinfo("Voice Settings", "Voice settings opened")
    
    def test_microphone(self):
        self.add_conversation_message("SYSTEM", "Microphone test: Recording for 3 seconds...")
    
    def volume_control(self):
        messagebox.showinfo("Volume Control", "Volume control panel opened")
    
    def power_options(self):
        messagebox.showinfo("Power Options", "Power options panel opened")
    
    def ai_chat(self):
        messagebox.showinfo("AI Chat", "AI chat interface opened")
    
    def memory_manager(self):
        messagebox.showinfo("Memory Manager", "Memory manager opened")
    
    def ai_settings(self):
        messagebox.showinfo("AI Settings", "AI settings panel opened")
    
    def clear_history(self):
        self.conversation_text.delete(1.0, tk.END)
        self.add_conversation_message("SYSTEM", "Conversation history cleared")
    
    def plugin_manager(self):
        messagebox.showinfo("Plugin Manager", "Plugin manager opened")
    
    def timer_control(self):
        messagebox.showinfo("Timer Control", "Timer control panel opened")
    
    def file_operations(self):
        messagebox.showinfo("File Operations", "File operations panel opened")
    
    def network_monitor(self):
        messagebox.showinfo("Network Monitor", "Network monitor opened")
    
    def toggle_plugin(self, plugin):
        current_status = plugin['status']
        new_status = 'Disabled' if current_status == 'Enabled' else 'Enabled'
        self.add_conversation_message("SYSTEM", f"Plugin '{plugin['name']}' {new_status.lower()}")
    
    def save_settings(self):
        messagebox.showinfo("Settings", "Settings saved successfully!")
        self.add_conversation_message("SYSTEM", "Settings saved")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing"""
        self.system_monitor_active = False
        self.root.destroy()

if __name__ == "__main__":
    app = FuturisticVecnaControlPanel()
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.run()
