"""
Enhanced Vecna Voice Assistant with Advanced Features
- GUI Interface with System Tray
- Plugin System
- Advanced System Control
- Notifications and Scheduling
"""

from vecna import VecnaAssistant, Config
from vecna_plugin_system import PluginManager
from advanced_system_control import AdvancedSystemController
import threading
import time
import os

try:
    from vecna_gui import VecnaGUI
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("GUI not available. Install tkinter and PIL for GUI support.")

try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False

class EnhancedVecnaAssistant(VecnaAssistant):
    def __init__(self, use_gui=True):
        super().__init__()
        
        # Initialize new components
        self.plugin_manager = PluginManager()
        self.advanced_controller = AdvancedSystemController()
        self.use_gui = use_gui and GUI_AVAILABLE
        self.gui = None
        self.is_paused = False
        
        # Enhanced command mappings
        self.enhanced_commands = {
            # Window management
            "switch to": self._handle_switch_window,
            "minimize": self._handle_minimize,
            "close window": self._handle_close_specific_window,
            "list windows": self._handle_list_windows,
            
            # Process management
            "kill process": self._handle_kill_process,
            "list processes": self._handle_list_processes,
            
            # File operations
            "find file": self._handle_find_file,
            "create folder": self._handle_create_folder,
            "move file": self._handle_move_file,
            
            # Screenshots and recording
            "record screen": self._handle_screen_recording,
            "screenshot window": self._handle_window_screenshot,
            
            # Timers
            "set timer": self._handle_set_timer,
            "list timers": self._handle_list_timers,
            "cancel timer": self._handle_cancel_timer,
            
            # System info
            "detailed system info": self._handle_detailed_system_info,
            "network status": self._handle_network_status,
            "wifi networks": self._handle_wifi_networks,
            
            # Plugin commands
            "list plugins": self._handle_list_plugins,
            "enable plugin": self._handle_enable_plugin,
            "disable plugin": self._handle_disable_plugin,
            
            # Assistant control
            "pause listening": self._handle_pause,
            "resume listening": self._handle_resume,
            "show gui": self._handle_show_gui,
            "hide gui": self._handle_hide_gui,
        }
    
    # ========== Window Management Handlers ==========
    def _handle_switch_window(self, command):
        window_name = command.replace("switch to", "").strip()
        return self.advanced_controller.switch_to_window(window_name)
    
    def _handle_minimize(self, command):
        if "current" in command or "this" in command:
            return self.advanced_controller.minimize_window()
        else:
            window_name = command.replace("minimize", "").strip()
            return self.advanced_controller.minimize_window(window_name)
    
    def _handle_close_specific_window(self, command):
        window_name = command.replace("close window", "").strip()
        if window_name:
            return self.advanced_controller.close_window(window_name)
        else:
            return self.advanced_controller.close_window()
    
    def _handle_list_windows(self, command):
        windows = self.advanced_controller.get_all_windows()
        if windows:
            window_list = "Open windows: " + ", ".join([w['title'] for w in windows[:10]])
            return window_list
        else:
            return "No windows found"
    
    # ========== Process Management Handlers ==========
    def _handle_kill_process(self, command):
        process_name = command.replace("kill process", "").strip()
        return self.advanced_controller.kill_process(process_name)
    
    def _handle_list_processes(self, command):
        processes = self.advanced_controller.list_running_processes()
        if processes:
            process_list = "Top processes by CPU: "
            for proc in processes[:5]:
                process_list += f"{proc['name']} ({proc['cpu_percent']:.1f}%), "
            return process_list.rstrip(", ")
        else:
            return "No processes found"
    
    # ========== File Operation Handlers ==========
    def _handle_find_file(self, command):
        filename = command.replace("find file", "").strip()
        return self.advanced_controller.find_files(filename)
    
    def _handle_create_folder(self, command):
        folder_path = command.replace("create folder", "").strip()
        return self.advanced_controller.create_folder(folder_path)
    
    def _handle_move_file(self, command):
        # This would need more sophisticated parsing
        return "Move file command needs source and destination. Example: 'move file from Downloads to Desktop'"
    
    # ========== Screenshot and Recording Handlers ==========
    def _handle_screen_recording(self, command):
        # Extract duration if specified
        duration = 30  # default
        words = command.split()
        for i, word in enumerate(words):
            if word.isdigit():
                duration = int(word)
                break
        
        return self.advanced_controller.start_screen_recording(duration)
    
    def _handle_window_screenshot(self, command):
        window_name = command.replace("screenshot window", "").strip()
        return self.advanced_controller.take_window_screenshot(window_name)
    
    # ========== Timer Handlers ==========
    def _handle_set_timer(self, command):
        # Extract minutes and message
        words = command.split()
        minutes = 5  # default
        message = "Timer finished!"
        
        for i, word in enumerate(words):
            if word.isdigit():
                minutes = int(word)
                # Get message after the number
                if i + 2 < len(words):  # Skip "minutes" word
                    message = " ".join(words[i + 2:])
                break
        
        return self.advanced_controller.set_timer(minutes, message)
    
    def _handle_list_timers(self, command):
        return self.advanced_controller.list_timers()
    
    def _handle_cancel_timer(self, command):
        message_part = command.replace("cancel timer", "").strip()
        return self.advanced_controller.cancel_timer(message_part)
    
    # ========== System Info Handlers ==========
    def _handle_detailed_system_info(self, command):
        info = self.advanced_controller.get_detailed_system_info()
        response = f"CPU: {info['cpu']['usage']}%, Memory: {info['memory']['percentage']}%, "
        response += f"Disk: {info['disk']['percentage']:.1f}%"
        if info['battery'] != "No battery":
            response += f", Battery: {info['battery']['percentage']}%"
        return response
    
    def _handle_network_status(self, command):
        status = self.advanced_controller.get_network_status()
        response = f"Internet: {'Connected' if status['internet_connected'] else 'Disconnected'}"
        if status['active_interfaces']:
            response += f", Active interfaces: {len(status['active_interfaces'])}"
        return response
    
    def _handle_wifi_networks(self, command):
        return self.advanced_controller.get_wifi_networks()
    
    # ========== Plugin Handlers ==========
    def _handle_list_plugins(self, command):
        plugins = self.plugin_manager.get_plugin_info()
        if plugins:
            plugin_list = "Available plugins: "
            for name, info in plugins.items():
                status = "enabled" if info['enabled'] else "disabled"
                plugin_list += f"{name} ({status}), "
            return plugin_list.rstrip(", ")
        else:
            return "No plugins loaded"
    
    def _handle_enable_plugin(self, command):
        plugin_name = command.replace("enable plugin", "").strip()
        if self.plugin_manager.enable_plugin(plugin_name):
            return f"Enabled plugin: {plugin_name}"
        else:
            return f"Plugin '{plugin_name}' not found"
    
    def _handle_disable_plugin(self, command):
        plugin_name = command.replace("disable plugin", "").strip()
        if self.plugin_manager.disable_plugin(plugin_name):
            return f"Disabled plugin: {plugin_name}"
        else:
            return f"Plugin '{plugin_name}' not found"
    
    # ========== Assistant Control Handlers ==========
    def _handle_pause(self, command):
        self.is_paused = True
        return "Paused listening. Say 'resume listening' to continue."
    
    def _handle_resume(self, command):
        self.is_paused = False
        return "Resumed listening."
    
    def _handle_show_gui(self, command):
        if self.gui:
            self.gui.show_from_tray()
            return "Showing GUI"
        else:
            return "GUI not available"
    
    def _handle_hide_gui(self, command):
        if self.gui:
            self.gui.hide_to_tray()
            return "Hiding GUI to system tray"
        else:
            return "GUI not available"
    
    # ========== Enhanced Command Processing ==========
    def process_enhanced_command(self, command):
        """Process command with enhanced features first"""
        
        # Check if paused
        if self.is_paused and "resume listening" not in command.lower():
            return None
        
        # Try plugin commands first
        plugin_result = self.plugin_manager.execute_plugin_command(command, {
            'vecna': self,
            'system_controller': self.advanced_controller
        })
        
        if plugin_result:
            return plugin_result, None
        
        # Try enhanced commands
        for key_phrase, handler in self.enhanced_commands.items():
            if key_phrase.lower() in command.lower():
                try:
                    response = handler(command.lower())
                    return response, None
                except Exception as e:
                    return f"Error executing {key_phrase}: {e}", None
        
        # Fall back to original command processing
        return self.command_processor.process_command(command)
    
    def show_notification(self, title, message):
        """Show system notification"""
        if NOTIFICATIONS_AVAILABLE:
            try:
                notification.notify(
                    title=title,
                    message=message,
                    timeout=3
                )
            except Exception as e:
                print(f"Notification error: {e}")
    
    def run_with_gui(self):
        """Run Vecna with GUI interface"""
        if not GUI_AVAILABLE:
            print("GUI not available. Running in console mode.")
            return self.run()
        
        # Initialize GUI
        self.gui = VecnaGUI(self)
        
        # Start Vecna in separate thread
        vecna_thread = threading.Thread(target=self.run_enhanced, daemon=True)
        vecna_thread.start()
        
        # Run GUI in main thread
        self.gui.run()
    
    def run_enhanced(self):
        """Enhanced run method with new features"""
        self.startup()
        self.speech_engine.speak("Enhanced Vecna initialized with advanced features.")
        
        # Show notification
        self.show_notification("Vecna", "Voice assistant started")
        
        # Update GUI if available
        if self.gui:
            self.gui.update_status("🎤 Listening...")
        
        while True:
            try:
                if not self.is_paused:
                    print("🎤 Listening for command...")
                    audio = self.recognizer.listen()
                    command = self.recognizer.recognize(audio)
                    
                    if command:
                        print(f"You said: {command}")
                        
                        # Update GUI
                        if self.gui:
                            self.gui.add_message("You", command)
                        
                        # Process with enhanced features
                        response, action = self.process_enhanced_command(command)
                        
                        if response:
                            # Save the interaction to memory
                            self.memory.add_conversation(command, response)
                            
                            # Update GUI
                            if self.gui:
                                self.gui.add_message("Vecna", response)
                            
                            # Speak the response
                            self.speech_engine.speak(response)
                            
                            # Execute any actions
                            if action:
                                try:
                                    exec(action)
                                except Exception as e:
                                    error_msg = f"Error executing action: {e}"
                                    print(error_msg)
                                    if self.gui:
                                        self.gui.add_message("System", error_msg)
                else:
                    time.sleep(1)  # Sleep when paused
                    
            except Exception as e:
                error_msg = f"Error in main loop: {e}"
                print(error_msg)
                if self.gui:
                    self.gui.add_message("System", error_msg)
                time.sleep(1)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Vecna Voice Assistant')
    parser.add_argument('--no-gui', action='store_true', help='Run without GUI')
    parser.add_argument('--create-plugins', action='store_true', help='Create example plugins')
    
    args = parser.parse_args()
    
    # Create example plugins if requested
    if args.create_plugins:
        from vecna_plugin_system import create_example_plugins
        create_example_plugins()
        print("Example plugins created in the plugins directory")
        return
    
    # Initialize enhanced Vecna
    vecna = EnhancedVecnaAssistant()
    
    if args.no_gui or not GUI_AVAILABLE:
        print("Starting Vecna in console mode...")
        vecna.run_enhanced()
    else:
        print("Starting Vecna with GUI...")
        vecna.run_with_gui()

if __name__ == "__main__":
    main()
