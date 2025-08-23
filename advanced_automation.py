"""
Advanced Automation Module for Vecna
Provides mouse automation, web scraping, and advanced system control
"""

import pyautogui
import time
import requests
from bs4 import BeautifulSoup
import subprocess
import os
import glob
import json
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading

# Configure pyautogui for safety
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1  # Small pause between actions

class AdvancedAutomation:
    def __init__(self):
        self.browser = None
        self.current_page = None
        self.automation_active = False
        
    # ====== ENHANCED APP LAUNCHER ======
    def open_advanced_app(self, app_name):
        """Enhanced app launcher with smart detection"""
        enhanced_apps = {
            "whatsapp": [
                "C:\\Users\\%USERNAME%\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
                "C:\\Program Files\\WhatsApp\\WhatsApp.exe",
                "C:\\Program Files (x86)\\WhatsApp\\WhatsApp.exe"
            ],
            "davinci": [
                "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\Resolve.exe",
                "C:\\Program Files (x86)\\Blackmagic Design\\DaVinci Resolve\\Resolve.exe"
            ],
            "davinci resolve": [
                "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\Resolve.exe"
            ],
            "telegram": [
                "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe"
            ],
            "discord": [
                "C:\\Users\\%USERNAME%\\AppData\\Local\\Discord\\app-*\\Discord.exe"
            ],
            "spotify": [
                "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe",
                "C:\\Program Files\\Spotify\\Spotify.exe"
            ],
            "steam": [
                "C:\\Program Files (x86)\\Steam\\steam.exe",
                "C:\\Program Files\\Steam\\steam.exe"
            ],
            "zoom": [
                "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"
            ],
            "microsoft teams": [
                "C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe"
            ],
            "vlc": [
                "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
                "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
            ],
            "obs": [
                "C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe"
            ],
            "photoshop": [
                "C:\\Program Files\\Adobe\\Adobe Photoshop *\\Photoshop.exe"
            ],
            "premiere": [
                "C:\\Program Files\\Adobe\\Adobe Premiere Pro *\\Adobe Premiere Pro.exe"
            ],
            "after effects": [
                "C:\\Program Files\\Adobe\\Adobe After Effects *\\Support Files\\AfterFX.exe"
            ],
            "blender": [
                "C:\\Program Files\\Blender Foundation\\Blender *\\blender.exe"
            ],
            "unity": [
                "C:\\Program Files\\Unity\\Hub\\Editor\\*\\Editor\\Unity.exe"
            ],
            "visual studio": [
                "C:\\Program Files\\Microsoft Visual Studio\\*\\*\\Common7\\IDE\\devenv.exe"
            ],
            "firefox": [
                "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
            ],
            "edge": [
                "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
            ],
            "brave": [
                "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
            ],
            "notepad++": [
                "C:\\Program Files\\Notepad++\\notepad++.exe",
                "C:\\Program Files (x86)\\Notepad++\\notepad++.exe"
            ],
            "7zip": [
                "C:\\Program Files\\7-Zip\\7zFM.exe",
                "C:\\Program Files (x86)\\7-Zip\\7zFM.exe"
            ]
        }
        
        # Find matching app
        app_name_lower = app_name.lower()
        matched_apps = [key for key in enhanced_apps.keys() if key in app_name_lower]
        
        if matched_apps:
            app_key = matched_apps[0]
            app_paths = enhanced_apps[app_key]
            
            for path in app_paths:
                try:
                    expanded_path = os.path.expandvars(path)
                    
                    # Handle wildcard paths
                    if '*' in expanded_path:
                        matching_paths = glob.glob(expanded_path)
                        if matching_paths:
                            subprocess.Popen(matching_paths[0])
                            return f"Successfully opened {app_key}"
                    elif os.path.exists(expanded_path):
                        subprocess.Popen(expanded_path)
                        return f"Successfully opened {app_key}"
                except Exception as e:
                    print(f"Failed to open {path}: {e}")
                    continue
            
            # If no direct path worked, try Windows search
            try:
                subprocess.run(f'start "" "{app_key}"', shell=True, check=True)
                return f"Attempting to open {app_key} via Windows search"
            except subprocess.CalledProcessError:
                return f"Could not find {app_key} on this system"
        else:
            # Try generic Windows search
            try:
                subprocess.run(f'start "" "{app_name}"', shell=True, check=True)
                return f"Attempting to open {app_name}"
            except subprocess.CalledProcessError:
                return f"Could not find application: {app_name}"
    
    # ====== MOUSE AUTOMATION ======
    def move_mouse_to(self, x, y):
        """Move mouse to specific coordinates"""
        try:
            pyautogui.moveTo(x, y, duration=0.5)
            return f"Moved mouse to ({x}, {y})"
        except Exception as e:
            return f"Error moving mouse: {e}"
    
    def click_at(self, x, y):
        """Click at specific coordinates"""
        try:
            pyautogui.click(x, y)
            return f"Clicked at ({x}, {y})"
        except Exception as e:
            return f"Error clicking: {e}"
    
    def double_click_at(self, x, y):
        """Double click at specific coordinates"""
        try:
            pyautogui.doubleClick(x, y)
            return f"Double clicked at ({x}, {y})"
        except Exception as e:
            return f"Error double clicking: {e}"
    
    def right_click_at(self, x, y):
        """Right click at specific coordinates"""
        try:
            pyautogui.rightClick(x, y)
            return f"Right clicked at ({x}, {y})"
        except Exception as e:
            return f"Error right clicking: {e}"
    
    def drag_mouse(self, start_x, start_y, end_x, end_y):
        """Drag from start to end coordinates"""
        try:
            pyautogui.drag(end_x - start_x, end_y - start_y, duration=1, button='left')
            return f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})"
        except Exception as e:
            return f"Error dragging: {e}"
    
    def scroll_at(self, x, y, clicks=3):
        """Scroll at specific location"""
        try:
            pyautogui.scroll(clicks, x=x, y=y)
            direction = "up" if clicks > 0 else "down"
            return f"Scrolled {direction} at ({x}, {y})"
        except Exception as e:
            return f"Error scrolling: {e}"
    
    def find_and_click_image(self, image_path, confidence=0.8):
        """Find an image on screen and click it"""
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                pyautogui.click(center)
                return f"Found and clicked image at {center}"
            else:
                return f"Image not found on screen: {image_path}"
        except Exception as e:
            return f"Error finding image: {e}"
    
    def get_mouse_position(self):
        """Get current mouse position"""
        try:
            x, y = pyautogui.position()
            return f"Mouse position: ({x}, {y})"
        except Exception as e:
            return f"Error getting mouse position: {e}"
    
    def automate_typing(self, text, interval=0.05):
        """Type text with natural intervals"""
        try:
            pyautogui.typewrite(text, interval=interval)
            return f"Typed: {text}"
        except Exception as e:
            return f"Error typing: {e}"
    
    def send_hotkey(self, *keys):
        """Send keyboard hotkey combination"""
        try:
            pyautogui.hotkey(*keys)
            return f"Sent hotkey: {' + '.join(keys)}"
        except Exception as e:
            return f"Error sending hotkey: {e}"
    
    def screenshot_region(self, x, y, width, height, filename=None):
        """Take screenshot of specific region"""
        try:
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            if filename:
                screenshot.save(filename)
                return f"Screenshot saved: {filename}"
            else:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_region_{timestamp}.png"
                screenshot.save(filename)
                return f"Screenshot saved: {filename}"
        except Exception as e:
            return f"Error taking screenshot: {e}"
    
    # ====== WEB AUTOMATION ======
    def start_browser_automation(self, headless=False):
        """Start browser automation session"""
        try:
            options = Options()
            if headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            self.browser = webdriver.Chrome(options=options)
            self.automation_active = True
            return "Browser automation started"
        except Exception as e:
            return f"Error starting browser: {e}"
    
    def navigate_to_website(self, url):
        """Navigate to a website"""
        if not self.browser:
            self.start_browser_automation()
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.browser.get(url)
            self.current_page = url
            return f"Navigated to {url}"
        except Exception as e:
            return f"Error navigating to website: {e}"
    
    def find_and_click_element(self, by_type, value):
        """Find and click web element"""
        if not self.browser:
            return "Browser not started"
        
        try:
            if by_type.lower() == 'id':
                element = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.ID, value))
                )
            elif by_type.lower() == 'class':
                element = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, value))
                )
            elif by_type.lower() == 'xpath':
                element = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, value))
                )
            elif by_type.lower() == 'text':
                element = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, value))
                )
            elif by_type.lower() == 'tag':
                element = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.TAG_NAME, value))
                )
            else:
                return f"Unknown selector type: {by_type}"
            
            element.click()
            return f"Clicked element: {by_type}={value}"
        except Exception as e:
            return f"Error clicking element: {e}"
    
    def fill_form_field(self, by_type, value, text):
        """Fill a form field with text"""
        if not self.browser:
            return "Browser not started"
        
        try:
            if by_type.lower() == 'id':
                element = self.browser.find_element(By.ID, value)
            elif by_type.lower() == 'name':
                element = self.browser.find_element(By.NAME, value)
            elif by_type.lower() == 'xpath':
                element = self.browser.find_element(By.XPATH, value)
            else:
                return f"Unknown selector type for form: {by_type}"
            
            element.clear()
            element.send_keys(text)
            return f"Filled field {value} with: {text}"
        except Exception as e:
            return f"Error filling form field: {e}"
    
    def scrape_page_content(self):
        """Scrape current page content"""
        if not self.browser:
            return "Browser not started"
        
        try:
            page_source = self.browser.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract useful information
            title = soup.title.string if soup.title else "No title"
            headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3'])]
            links = [{'text': a.get_text().strip(), 'url': a.get('href')} 
                    for a in soup.find_all('a', href=True)]
            
            return {
                'title': title,
                'headings': headings[:10],  # First 10 headings
                'links': links[:10],  # First 10 links
                'url': self.current_page
            }
        except Exception as e:
            return f"Error scraping page: {e}"
    
    def search_on_google(self, query):
        """Perform Google search"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            result = self.navigate_to_website(search_url)
            if "Error" not in result:
                time.sleep(2)  # Wait for page load
                return f"Searched Google for: {query}"
            return result
        except Exception as e:
            return f"Error searching Google: {e}"
    
    def close_browser(self):
        """Close browser automation"""
        try:
            if self.browser:
                self.browser.quit()
                self.browser = None
                self.automation_active = False
                return "Browser closed"
            return "Browser was not running"
        except Exception as e:
            return f"Error closing browser: {e}"
    
    # ====== ADVANCED SYSTEM OPERATIONS ======
    def automate_file_operation(self, operation, source=None, destination=None):
        """Automate file operations"""
        try:
            if operation.lower() == "copy":
                import shutil
                shutil.copy2(source, destination)
                return f"Copied {source} to {destination}"
            elif operation.lower() == "move":
                import shutil
                shutil.move(source, destination)
                return f"Moved {source} to {destination}"
            elif operation.lower() == "delete":
                os.remove(source)
                return f"Deleted {source}"
            elif operation.lower() == "create_folder":
                os.makedirs(source, exist_ok=True)
                return f"Created folder: {source}"
            else:
                return f"Unknown file operation: {operation}"
        except Exception as e:
            return f"Error in file operation: {e}"
    
    def automate_window_management(self, operation, window_title=None):
        """Automate window management"""
        try:
            import pygetwindow as gw
            
            if operation.lower() == "list_windows":
                windows = gw.getAllTitles()
                return f"Open windows: {', '.join(windows[:10])}"  # First 10
            
            elif operation.lower() == "focus_window" and window_title:
                windows = gw.getWindowsWithTitle(window_title)
                if windows:
                    windows[0].activate()
                    return f"Focused window: {window_title}"
                return f"Window not found: {window_title}"
            
            elif operation.lower() == "minimize_window" and window_title:
                windows = gw.getWindowsWithTitle(window_title)
                if windows:
                    windows[0].minimize()
                    return f"Minimized window: {window_title}"
                return f"Window not found: {window_title}"
            
            elif operation.lower() == "maximize_window" and window_title:
                windows = gw.getWindowsWithTitle(window_title)
                if windows:
                    windows[0].maximize()
                    return f"Maximized window: {window_title}"
                return f"Window not found: {window_title}"
            
            else:
                return f"Unknown window operation: {operation}"
        except Exception as e:
            return f"Error in window management: {e}"
    
    def create_automation_script(self, actions):
        """Create and execute automation script"""
        try:
            script_results = []
            for action in actions:
                if action['type'] == 'click':
                    result = self.click_at(action['x'], action['y'])
                elif action['type'] == 'type':
                    result = self.automate_typing(action['text'])
                elif action['type'] == 'wait':
                    time.sleep(action['seconds'])
                    result = f"Waited {action['seconds']} seconds"
                elif action['type'] == 'hotkey':
                    result = self.send_hotkey(*action['keys'])
                else:
                    result = f"Unknown action type: {action['type']}"
                
                script_results.append(result)
                time.sleep(0.1)  # Small delay between actions
            
            return f"Automation script completed: {len(script_results)} actions executed"
        except Exception as e:
            return f"Error executing automation script: {e}"

# Global automation instance
automation = AdvancedAutomation()
