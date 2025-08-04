# VECNA Voice Assistant

A powerful voice-controlled assistant for Windows that allows complete hands-free control of your system.

## Features

- **Wake word detection**: Activate by saying "Hey Vecna", "Hi Vecna" or "Okay Vecna"
- **Speech recognition**: Uses Google Speech Recognition or Whisper for accurate transcription
- **Natural voice responses**: Text-to-speech with customizable voices
- **System control**:
  - Open applications and folders
  - Type text, copy/paste
  - Control media playback
  - Adjust volume and brightness
  - Take screenshots
  - Web search
  - Lock computer
  - Much more!
- **Memory system**: Remembers conversations and preferences
- **AI integration**: Can use OpenAI GPT or Google Gemini for smarter responses
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
