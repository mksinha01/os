# Enhanced Vecna Voice Assistant 🎤🤖

A powerful Python-based voice assistant that transforms your Windows PC into a smart, voice-controlled system. Named "Vecna" for its comprehensive system control capabilities and AI-powered intelligence.

## 🌟 Features

### Core Features
- **Advanced Voice Recognition**: Multi-layered recognition with Google Speech API and Whisper AI
- **Natural Text-to-Speech**: High-quality voice responses using pyttsx3
- **No Wake Word**: Continuous listening for seamless interaction
- **AI Integration**: OpenAI GPT and Google Gemini support for intelligent conversations
- **Memory System**: Persistent conversation memory and learning

### System Control
- **Application Management**: Open, close, and control any Windows application
- **Window Management**: Switch, minimize, maximize, and arrange windows
- **Process Control**: Monitor and manage running processes
- **File Operations**: Create folders, find files, manage directories
- **System Functions**: Shutdown, restart, sleep, lock, volume control

### Advanced Features
- **GUI Interface**: Modern dark-theme interface with system tray integration
- **Plugin System**: Extensible architecture with custom plugin support
- **Screen Capture**: Screenshots and screen recording capabilities
- **Timer System**: Set multiple timers with custom messages
- **Network Monitoring**: WiFi status, network diagnostics
- **System Monitoring**: CPU, memory, disk, battery status

### Built-in Plugins
- **Weather Plugin**: Real-time weather information
- **Calculator Plugin**: Advanced mathematical calculations
- **Todo Plugin**: Task management and reminders

## 🚀 Quick Start

### Option 1: Easy Setup (Recommended)
1. **Run the startup script**:
   ```
   start_vecna.bat
   ```
   This will automatically set up the environment and install dependencies.

2. **Choose your preferred mode**:
   - Enhanced Vecna with GUI (recommended)
   - Enhanced Vecna without GUI
   - Simple Vecna (basic features)

### Option 2: Manual Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements_complete.txt
   ```

2. **Test Installation**:
   ```bash
   python test_vecna.py
   ```

3. **Run Enhanced Vecna**:
   ```bash
   python vecna_enhanced.py
   ```

## 🎯 Voice Commands

### Application Control
- "open notepad" / "open chrome" / "open calculator"
- "close window" / "close notepad"
- "switch to chrome"
- "minimize window" / "minimize current"
- "list windows"

### System Operations
- "screenshot" / "screenshot window chrome"
- "record screen for 30 seconds"
- "volume up" / "volume down" / "mute"
- "shutdown computer" / "restart computer"
- "lock computer" / "sleep computer"

### Process & System Monitoring
- "list processes"
- "kill process notepad"
- "detailed system info"
- "network status"
- "wifi networks"

### File & Folder Management
- "create folder Documents/NewProject"
- "find file document.txt"
- "type hello world"
- "search for python tutorials"

### Timer & Scheduling
- "set timer 5 minutes coffee break"
- "list timers"
- "cancel timer coffee"

### Plugin Commands
- "what's the weather in New York" (Weather plugin)
- "calculate 25 * 30 + 15" (Calculator plugin)
- "add task buy groceries" (Todo plugin)
- "list plugins"
- "enable plugin weather"

### Assistant Control
- "pause listening"
- "resume listening"
- "show gui"
- "hide gui"

### AI-Powered Conversations
- "what is artificial intelligence"
- "tell me a joke"
- "explain quantum computing"
- "write a short story"

## ⚙️ Configuration

### Environment Variables (Optional)
Create a `.env` file for AI features:
```
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

### Configuration File
Customize settings in `config.json`:
- Speech recognition sensitivity
- AI model preferences
- GUI themes and appearance
- Plugin settings
- Hotkey combinations

## 📁 Project Structure

```
vecna-assistant/
├── vecna.py                     # Core voice assistant
├── vecna_enhanced.py            # Enhanced version with all features
├── vecna_simple.py              # Lightweight version
├── vecna_gui.py                 # GUI interface
├── vecna_plugin_system.py       # Plugin architecture
├── advanced_system_control.py   # Advanced Windows control
├── start_vecna.bat             # Easy startup script
├── test_vecna.py               # System test script
├── config.json                 # Configuration file
├── requirements_complete.txt    # All dependencies
├── vecna_memory.json           # Conversation memory
└── plugins/                    # Plugin directory
    ├── weather_plugin.py
    ├── calculator_plugin.py
    └── todo_plugin.py
```

## 🛠️ Available Versions

### 1. Enhanced Vecna (`vecna_enhanced.py`)
- **Full Feature Set**: GUI, plugins, advanced system control
- **Best For**: Power users wanting maximum functionality
- **Requirements**: All dependencies from `requirements_complete.txt`

### 2. Simple Vecna (`vecna_simple.py`)
- **Lightweight**: Core features with minimal dependencies
- **Best For**: Basic voice control and older systems
- **Requirements**: Only core dependencies

### 3. Original Vecna (`vecna.py`)
- **Balanced**: Full voice features without GUI overhead
- **Best For**: Users wanting comprehensive voice control
- **Requirements**: Standard dependencies

## 🔧 Troubleshooting

### Installation Issues

**PyAudio Installation Problems:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Windows-specific Dependencies:**
```bash
pip install pywin32
pip install comtypes
```

### Voice Recognition Issues

1. **Check Microphone Permissions**
   - Windows Settings → Privacy → Microphone
   - Enable microphone access for applications

2. **Adjust Recognition Settings**
   - Modify `energy_threshold` in `config.json`
   - Try different recognition engines (Google, Whisper)

3. **Network Issues**
   - Ensure stable internet connection
   - Whisper works offline as fallback

### Performance Optimization

1. **Use Appropriate Version**
   - Simple version for basic functionality
   - Enhanced version for full features

2. **Adjust Settings**
   - Lower speech recognition timeout
   - Disable unused plugins
   - Reduce GUI update frequency

### Common Fixes

**GUI Not Starting:**
- Install tkinter: `pip install tk`
- Install Pillow: `pip install Pillow`

**Plugin Errors:**
- Check plugin directory permissions
- Verify plugin dependencies
- Disable problematic plugins in config

## 🔐 Security & Privacy

- **Local Processing**: Core functionality works offline
- **API Usage**: AI features require internet (optional)
- **Data Storage**: Conversations stored locally in JSON format
- **Permissions**: Requires microphone and system control permissions

## 📋 System Requirements

- **OS**: Windows 10/11 (64-bit recommended)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB for full installation
- **Audio**: Working microphone and speakers
- **Network**: Internet connection for AI features (optional)

## 🔄 Updates & Maintenance

### Updating Dependencies
```bash
pip install -r requirements_complete.txt --upgrade
```

### Backing Up Settings
```bash
copy config.json config_backup.json
copy vecna_memory.json memory_backup.json
```

### Plugin Management
- Add new plugins to the `plugins/` directory
- Enable/disable plugins via voice commands or GUI
- Create custom plugins using the provided template

## 🤝 Contributing

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Plugin Development
- Use `vecna_plugin_system.py` as reference
- Follow the VecnaPlugin base class structure
- Submit plugins for inclusion in the main project

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT API
- **Google** for Speech Recognition API
- **OpenAI Whisper** for offline speech recognition
- **Python Community** for excellent libraries

## 📞 Support

- **Issues**: Report bugs via GitHub Issues
- **Questions**: Start a GitHub Discussion
- **Features**: Submit feature requests with detailed descriptions

---

**Made with ❤️ for voice-controlled computing**
- **Customizable**: Add your own commands and configure settings

## Installation

1. Install Python 3.8+ if you don't have it already
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Optional: Set your API keys in the Config class inside `vecna.py` if you want to use AI features
4. Run the assistant:
   ```
   python vecna.py
   ```

## Usage

1. Start the assistant by running `python vecna.py`
2. Say "Hey Vecna" to activate
3. When Vecna responds with "Yes?", speak your command
4. Example commands:
   - "Open Chrome"
   - "Open downloads folder"
   - "What's the time?"
   - "Set volume to 50 percent"
   - "Search for weather in New York"
   - "Take a screenshot"
   - "Lock my computer"
   - "Type hello world"
   - "Copy this text"

## Customization

Edit the `Config` class in `vecna.py` to:
- Change the wake words
- Configure voice settings
- Set API keys
- Add custom application paths
- Enable/disable features

## Requirements

- Windows 10/11
- Python 3.8+
- Working microphone
- Internet connection (for some features)

## Known Issues

- Some commands may require admin privileges
- Speech recognition accuracy varies with microphone quality and background noise
- Wake word detection may sometimes trigger on similar sounds

## Future Enhancements

- GUI interface with system tray icon
- More AI integrations
- Custom plugin system
- Better offline support
