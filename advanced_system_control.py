import os
import json
import time
import threading
import subprocess
import psutil
import win32gui
import win32con
import win32api
import win32clipboard
from PIL import ImageGrab
import cv2
import numpy as np
from datetime import datetime, timedelta

class AdvancedSystemController:
    def __init__(self):
        self.scheduled_tasks = []
        self.running_timers = {}
        
    # ========== Window Management ==========
    def get_all_windows(self):
        """Get list of all open windows"""
        windows = []
        
        def enum_handler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if window_text:
                    windows.append({
                        'hwnd': hwnd,
                        'title': window_text,
                        'class': win32gui.GetClassName(hwnd)
                    })
        
        win32gui.EnumWindows(enum_handler, None)
        return windows
    
    def switch_to_window(self, window_name):
        """Switch to specific window by name"""
        windows = self.get_all_windows()
        
        for window in windows:
            if window_name.lower() in window['title'].lower():
                hwnd = window['hwnd']
                # Restore if minimized
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                # Bring to foreground
                win32gui.SetForegroundWindow(hwnd)
                return f"Switched to {window['title']}"
        
        return f"Window containing '{window_name}' not found"
    
    def minimize_window(self, window_name=None):
        """Minimize specific window or current window"""
        if window_name:
            windows = self.get_all_windows()
            for window in windows:
                if window_name.lower() in window['title'].lower():
                    win32gui.ShowWindow(window['hwnd'], win32con.SW_MINIMIZE)
                    return f"Minimized {window['title']}"
            return f"Window '{window_name}' not found"
        else:
            # Minimize current foreground window
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return "Minimized current window"
    
    def close_window(self, window_name=None):
        """Close specific window or current window"""
        if window_name:
            windows = self.get_all_windows()
            for window in windows:
                if window_name.lower() in window['title'].lower():
                    win32gui.PostMessage(window['hwnd'], win32con.WM_CLOSE, 0, 0)
                    return f"Closed {window['title']}"
            return f"Window '{window_name}' not found"
        else:
            # Close current foreground window
            hwnd = win32gui.GetForegroundWindow()
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            return "Closed current window"
    
    # ========== Process Management ==========
    def list_running_processes(self):
        """List all running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        return processes[:10]  # Return top 10
    
    def kill_process(self, process_name):
        """Kill process by name"""
        killed = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    killed.append(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if killed:
            return f"Killed processes: {', '.join(killed)}"
        else:
            return f"No process found containing '{process_name}'"
    
    # ========== Advanced File Operations ==========
    def find_files(self, filename, search_path=None):
        """Find files by name"""
        if search_path is None:
            search_path = os.path.expanduser("~")
        
        found_files = []
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if filename.lower() in file.lower():
                    found_files.append(os.path.join(root, file))
                    if len(found_files) >= 10:  # Limit results
                        break
            if len(found_files) >= 10:
                break
        
        if found_files:
            return f"Found {len(found_files)} files:\\n" + "\\n".join(found_files)
        else:
            return f"No files found containing '{filename}'"
    
    def create_folder(self, folder_path):
        """Create a new folder"""
        try:
            os.makedirs(folder_path, exist_ok=True)
            return f"Created folder: {folder_path}"
        except Exception as e:
            return f"Error creating folder: {e}"
    
    def move_file(self, source, destination):
        """Move file from source to destination"""
        try:
            import shutil
            shutil.move(source, destination)
            return f"Moved {source} to {destination}"
        except Exception as e:
            return f"Error moving file: {e}"
    
    # ========== Screen Recording and Screenshots ==========
    def start_screen_recording(self, duration=30):
        """Start screen recording for specified duration"""
        def record_screen():
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            screen_size = (1920, 1080)  # Adjust based on your screen
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screen_recording_{timestamp}.avi"
            
            out = cv2.VideoWriter(filename, fourcc, 20.0, screen_size)
            
            start_time = time.time()
            while (time.time() - start_time) < duration:
                # Capture screenshot
                screenshot = ImageGrab.grab()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                frame = cv2.resize(frame, screen_size)
                
                out.write(frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            out.release()
            cv2.destroyAllWindows()
            return filename
        
        threading.Thread(target=record_screen, daemon=True).start()
        return f"Started screen recording for {duration} seconds"
    
    def take_window_screenshot(self, window_name):
        """Take screenshot of specific window"""
        windows = self.get_all_windows()
        
        for window in windows:
            if window_name.lower() in window['title'].lower():
                hwnd = window['hwnd']
                
                # Get window dimensions
                rect = win32gui.GetWindowRect(hwnd)
                x, y, x1, y1 = rect
                
                # Take screenshot of specific region
                screenshot = ImageGrab.grab(bbox=(x, y, x1, y1))
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"window_screenshot_{timestamp}.png"
                screenshot.save(filename)
                
                return f"Screenshot of {window['title']} saved as {filename}"
        
        return f"Window '{window_name}' not found"
    
    # ========== Timers and Reminders ==========
    def set_timer(self, minutes, message="Timer finished!"):
        """Set a timer"""
        timer_id = str(int(time.time()))
        
        def timer_function():
            time.sleep(minutes * 60)
            if timer_id in self.running_timers:
                # Here you would typically show a notification or speak the message
                print(f"TIMER ALERT: {message}")
                del self.running_timers[timer_id]
        
        self.running_timers[timer_id] = {
            'start_time': datetime.now(),
            'duration': minutes,
            'message': message,
            'thread': threading.Thread(target=timer_function, daemon=True)
        }
        
        self.running_timers[timer_id]['thread'].start()
        
        return f"Timer set for {minutes} minutes: {message}"
    
    def list_timers(self):
        """List all running timers"""
        if not self.running_timers:
            return "No active timers"
        
        timer_list = "Active timers:\\n"
        for timer_id, timer_info in self.running_timers.items():
            elapsed = datetime.now() - timer_info['start_time']
            remaining = timer_info['duration'] - (elapsed.total_seconds() / 60)
            timer_list += f"- {timer_info['message']}: {remaining:.1f} minutes remaining\\n"
        
        return timer_list
    
    def cancel_timer(self, message_part):
        """Cancel timer by message"""
        for timer_id, timer_info in list(self.running_timers.items()):
            if message_part.lower() in timer_info['message'].lower():
                del self.running_timers[timer_id]
                return f"Cancelled timer: {timer_info['message']}"
        
        return f"No timer found containing '{message_part}'"
    
    # ========== System Information ==========
    def get_detailed_system_info(self):
        """Get comprehensive system information"""
        cpu_info = {
            'usage': psutil.cpu_percent(interval=1),
            'cores': psutil.cpu_count(),
            'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else 'Unknown'
        }
        
        memory = psutil.virtual_memory()
        memory_info = {
            'total': f"{memory.total / (1024**3):.1f} GB",
            'available': f"{memory.available / (1024**3):.1f} GB",
            'used': f"{memory.used / (1024**3):.1f} GB",
            'percentage': memory.percent
        }
        
        disk = psutil.disk_usage('/')
        disk_info = {
            'total': f"{disk.total / (1024**3):.1f} GB",
            'free': f"{disk.free / (1024**3):.1f} GB",
            'used': f"{disk.used / (1024**3):.1f} GB",
            'percentage': (disk.used / disk.total) * 100
        }
        
        # Network information
        network = psutil.net_io_counters()
        network_info = {
            'bytes_sent': f"{network.bytes_sent / (1024**2):.1f} MB",
            'bytes_recv': f"{network.bytes_recv / (1024**2):.1f} MB"
        }
        
        # Battery information
        battery = psutil.sensors_battery()
        battery_info = "No battery" if not battery else {
            'percentage': battery.percent,
            'plugged': battery.power_plugged,
            'time_left': str(timedelta(seconds=battery.secsleft)) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unknown"
        }
        
        return {
            'cpu': cpu_info,
            'memory': memory_info,
            'disk': disk_info,
            'network': network_info,
            'battery': battery_info
        }
    
    # ========== Network Operations ==========
    def get_network_status(self):
        """Get network connection status"""
        import socket
        
        def check_internet():
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                return True
            except OSError:
                return False
        
        # Get network interfaces
        interfaces = psutil.net_if_addrs()
        active_interfaces = []
        
        for interface, addresses in interfaces.items():
            for addr in addresses:
                if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                    active_interfaces.append({
                        'interface': interface,
                        'ip': addr.address,
                        'netmask': addr.netmask
                    })
        
        return {
            'internet_connected': check_internet(),
            'active_interfaces': active_interfaces
        }
    
    def get_wifi_networks(self):
        """Get available WiFi networks (Windows only)"""
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                networks = []
                for line in result.stdout.split('\\n'):
                    if 'All User Profile' in line:
                        network_name = line.split(':')[1].strip()
                        networks.append(network_name)
                
                return f"Available WiFi networks: {', '.join(networks)}"
            else:
                return "Could not retrieve WiFi networks"
                
        except Exception as e:
            return f"Error getting WiFi networks: {e}"

# Usage example
if __name__ == "__main__":
    controller = AdvancedSystemController()
    
    # Test some functions
    print("System Info:", controller.get_detailed_system_info())
    print("Network Status:", controller.get_network_status())
    print("Running Processes:", controller.list_running_processes()[:3])
