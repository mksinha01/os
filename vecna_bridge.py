"""
Vecna Bridge - Connection layer between Control Panel and Vecna Backend
This module provides a safe interface for the GUI to interact with Vecna
"""

import threading
import time
from typing import Optional, Callable, Dict, Any

# Import Vecna components safely
try:
    from vecna import (
        VecnaAssistant, Config, Memory, SpeechEngine, 
        SpeechRecognizer, SystemController, Intelligence, 
        CommandProcessor
    )
    VECNA_AVAILABLE = True
except ImportError as e:
    print(f"Vecna import error: {e}")
    VECNA_AVAILABLE = False

class VecnaBridge:
    """Bridge class to safely manage Vecna backend from GUI"""
    
    def __init__(self, message_callback: Optional[Callable] = None):
        self.message_callback = message_callback
        self.is_initialized = False
        self.is_listening = False
        self.listening_thread = None
        self.no_wake_word = False
        self.mic_index = None
        
        # Vecna components
        self.vecna_instance: Optional[VecnaAssistant] = None
        self.memory: Optional[Memory] = None
        self.speech_engine: Optional[SpeechEngine] = None
        self.recognizer: Optional[SpeechRecognizer] = None
        self.system_controller: Optional[SystemController] = None
        self.intelligence: Optional[Intelligence] = None
        self.command_processor: Optional[CommandProcessor] = None
        
    def initialize(self) -> bool:
        """Initialize Vecna components"""
        if not VECNA_AVAILABLE:
            self._log("Vecna modules not available")
            return False
            
        try:
            # Initialize core components
            self.memory = Memory()
            self.speech_engine = SpeechEngine()
            self.recognizer = SpeechRecognizer()
            self.system_controller = SystemController()
            self.intelligence = Intelligence(self.memory)
            self.command_processor = CommandProcessor(
                self.speech_engine,
                self.system_controller,
                self.memory,
                self.intelligence
            )
            
            # Create main Vecna instance
            self.vecna_instance = VecnaAssistant()
            
            self.is_initialized = True
            self._log("Vecna backend initialized successfully")
            return True
            
        except Exception as e:
            self._log(f"Failed to initialize Vecna: {e}")
            return False
    
    def start_listening(self) -> bool:
        """Start voice recognition loop"""
        if not self.is_initialized:
            self._log("Vecna not initialized")
            return False
            
        if self.is_listening:
            self._log("Already listening")
            return False
            
        try:
            self.is_listening = True
            self.listening_thread = threading.Thread(
                target=self._listening_loop, 
                daemon=True
            )
            self.listening_thread.start()
            
            self._log("Voice recognition started")
            if self.no_wake_word:
                self._speak("Listening for commands. No wake word required.")
            else:
                self._speak(f"Hello! I'm Vecna. Say '{Config.WAKE_WORDS[0]}' to get my attention.")
            return True
            
        except Exception as e:
            self._log(f"Failed to start listening: {e}")
            self.is_listening = False
            return False
    
    def stop_listening(self) -> bool:
        """Stop voice recognition loop"""
        if not self.is_listening:
            return False
            
        try:
            self.is_listening = False
            self._speak("Goodbye! Going offline now.")
            
            # Wait for thread to finish
            if self.listening_thread and self.listening_thread.is_alive():
                self.listening_thread.join(timeout=2)
            
            self._log("Voice recognition stopped")
            return True
            
        except Exception as e:
            self._log(f"Error stopping listening: {e}")
            return False
    
    def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a voice command and return result"""
        if not self.is_initialized:
            return {
                'success': False,
                'response': "Vecna not initialized",
                'error': True
            }
        
        try:
            if not self.command_processor:
                return {
                    'success': False,
                    'response': "Command processor unavailable",
                    'error': True
                }
            response, action = self.command_processor.process_command(command)
            
            result = {
                'success': True,
                'response': response or "Command executed",
                'action': action,
                'error': False
            }
            
            # Execute action if provided
            if action:
                try:
                    exec(action)
                    result['action_executed'] = True
                except Exception as e:
                    result['action_error'] = str(e)
                    result['action_executed'] = False
            
            # Speak response
            if response:
                self._speak(response)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'response': f"Error executing command: {e}",
                'error': True
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            'vecna_available': VECNA_AVAILABLE,
            'initialized': self.is_initialized,
            'listening': self.is_listening,
            'wake_words': Config.WAKE_WORDS if VECNA_AVAILABLE else [],
            'memory_entries': len(self.memory.memories.get('conversations', [])) if self.memory else 0
        }
    
    def get_conversation_history(self, limit: int = 10) -> list:
        """Get recent conversation history"""
        if not self.memory:
            return []
        
        conversations = self.memory.memories.get('conversations', [])
        return conversations[-limit:] if conversations else []
    
    def add_reminder(self, text: str, time_str: str) -> bool:
        """Add a reminder"""
        if not self.memory:
            return False
        
        try:
            self.memory.add_reminder(text, time_str)
            return True
        except Exception as e:
            self._log(f"Error adding reminder: {e}")
            return False
    
    def get_pending_reminders(self) -> list:
        """Get pending reminders"""
        if not self.memory:
            return []
        
        try:
            return self.memory.get_pending_reminders()
        except Exception as e:
            self._log(f"Error getting reminders: {e}")
            return []
    
    def configure_voice(self, rate: Optional[int] = None, volume: Optional[float] = None) -> bool:
        """Configure voice settings"""
        if not self.speech_engine:
            return False
        
        try:
            self.speech_engine.configure_voice(rate=rate, volume=volume)
            return True
        except Exception as e:
            self._log(f"Error configuring voice: {e}")
            return False
    
    def _listening_loop(self):
        """Main listening loop"""
        self._log("Listening loop started - say wake word to begin")
        
        while self.is_listening:
            try:
                # Listen for wake word unless disabled
                if self.no_wake_word or self._listen_for_wake_word():
                    self._log("Wake word detected! Listening for command...")
                    
                    # Listen for command
                    command = self._listen_for_command()
                    if command:
                        self._log(f"Command received: {command}")
                        
                        # Process command
                        result = self.execute_command(command)
                        
                        if result['success']:
                            self._log(f"Command executed: {result['response']}")
                        else:
                            self._log(f"Command failed: {result['response']}")
                
                time.sleep(0.1)  # Prevent CPU overuse
                
            except Exception as e:
                self._log(f"Error in listening loop: {e}")
                time.sleep(1)
    
    def _listen_for_wake_word(self) -> bool:
        """Listen for wake word"""
        if not self.recognizer:
            return False
        
        try:
            import speech_recognition as sr
            
            mic_kwargs = {}
            if self.mic_index is not None:
                mic_kwargs['device_index'] = self.mic_index
            with sr.Microphone(**mic_kwargs) as source:
                self.recognizer.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.recognizer.listen(source, phrase_time_limit=3)
            
            try:
                text = str(self.recognizer.recognizer.recognize_google(audio)).lower()
                for wake_word in Config.WAKE_WORDS:
                    if wake_word in text:
                        return True
                return False
            except sr.UnknownValueError:
                return False
            except sr.RequestError:
                return False
                
        except Exception as e:
            print(f"Wake word detection error: {e}")
            return False
    
    def _listen_for_command(self) -> Optional[str]:
        """Listen for voice command"""
        if not self.recognizer:
            return None
        
        try:
            import speech_recognition as sr
            
            mic_kwargs = {}
            if self.mic_index is not None:
                mic_kwargs['device_index'] = self.mic_index
            with sr.Microphone(**mic_kwargs) as source:
                self.recognizer.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            try:
                command = str(self.recognizer.recognizer.recognize_google(audio))
                return command
            except sr.UnknownValueError:
                self._log("Could not understand audio")
                return None
            except sr.RequestError as e:
                self._log(f"Recognition service error: {e}")
                return None
                
        except Exception as e:
            self._log(f"Command listening error: {e}")
            return None
    
    def _speak(self, text: str):
        """Safely speak text"""
        try:
            engine = self.speech_engine
            if engine and hasattr(engine, 'speak'):
                threading.Thread(
                    target=lambda: engine.speak(text), 
                    daemon=True
                ).start()
        except Exception as e:
            print(f"Speech error: {e}")
    
    def _log(self, message: str):
        """Log message to callback or console"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        if self.message_callback:
            try:
                self.message_callback("SYSTEM", message)
            except:
                pass
        
        print(formatted_message)

    # ===== Settings APIs for GUI =====
    def set_no_wake_word(self, enabled: bool):
        self.no_wake_word = bool(enabled)
        self._log(f"No-wake-word mode set to {self.no_wake_word}")

    def set_mic_index(self, index: Optional[int]):
        self.mic_index = index if (isinstance(index, int) and index >= 0) else None
        self._log(f"Microphone index set to {self.mic_index}")

# Convenience function to create bridge
def create_vecna_bridge(message_callback: Optional[Callable] = None) -> VecnaBridge:
    """Create and return a VecnaBridge instance"""
    return VecnaBridge(message_callback)
