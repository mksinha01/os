import importlib
import os
import inspect
from abc import ABC, abstractmethod
import json

class VecnaPlugin(ABC):
    """Base class for all Vecna plugins"""
    
    def __init__(self, name, description, version="1.0"):
        self.name = name
        self.description = description
        self.version = version
        self.enabled = True
        
    @abstractmethod
    def execute(self, command, context):
        """Execute the plugin functionality"""
        pass
    
    @abstractmethod
    def get_commands(self):
        """Return list of commands this plugin handles"""
        pass
    
    def get_info(self):
        """Return plugin information"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "enabled": self.enabled
        }

class PluginManager:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = {}
        self.command_map = {}
        
        # Create plugins directory if it doesn't exist
        if not os.path.exists(plugin_dir):
            os.makedirs(plugin_dir)
            
        self.load_plugins()
    
    def load_plugins(self):
        """Load all plugins from the plugins directory"""
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                try:
                    # Import the plugin module
                    spec = importlib.util.spec_from_file_location(
                        module_name, 
                        os.path.join(self.plugin_dir, filename)
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Find plugin classes in the module
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, VecnaPlugin) and 
                            obj != VecnaPlugin):
                            
                            plugin_instance = obj()
                            self.plugins[plugin_instance.name] = plugin_instance
                            
                            # Map commands to plugins
                            for command in plugin_instance.get_commands():
                                self.command_map[command.lower()] = plugin_instance
                            
                            print(f"Loaded plugin: {plugin_instance.name}")
                            
                except Exception as e:
                    print(f"Error loading plugin {filename}: {e}")
    
    def execute_plugin_command(self, command, context):
        """Execute a command using the appropriate plugin"""
        command_lower = command.lower()
        
        # Find matching plugin
        for cmd_pattern, plugin in self.command_map.items():
            if cmd_pattern in command_lower and plugin.enabled:
                try:
                    return plugin.execute(command, context)
                except Exception as e:
                    return f"Error executing plugin {plugin.name}: {e}"
        
        return None
    
    def get_all_commands(self):
        """Get all available plugin commands"""
        commands = {}
        for plugin in self.plugins.values():
            if plugin.enabled:
                commands[plugin.name] = plugin.get_commands()
        return commands
    
    def enable_plugin(self, plugin_name):
        """Enable a plugin"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].enabled = True
            return True
        return False
    
    def disable_plugin(self, plugin_name):
        """Disable a plugin"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].enabled = False
            return True
        return False
    
    def get_plugin_info(self):
        """Get information about all plugins"""
        return {name: plugin.get_info() for name, plugin in self.plugins.items()}

# Example plugins to get you started
example_weather_plugin = '''
import requests
from vecna_plugin_system import VecnaPlugin

class WeatherPlugin(VecnaPlugin):
    def __init__(self):
        super().__init__(
            name="Weather",
            description="Get weather information for any city",
            version="1.0"
        )
        self.api_key = "your_weather_api_key_here"  # Get from OpenWeatherMap
    
    def get_commands(self):
        return ["weather", "temperature", "forecast"]
    
    def execute(self, command, context):
        try:
            # Extract city name from command
            words = command.split()
            city = None
            for i, word in enumerate(words):
                if word.lower() in ["in", "for", "at"]:
                    city = " ".join(words[i+1:])
                    break
            
            if not city:
                return "Please specify a city. Example: 'weather in New York'"
            
            # Make API call (you'll need to get a free API key from OpenWeatherMap)
            if self.api_key == "your_weather_api_key_here":
                return f"Weather API key not configured. The weather in {city} is sunny and 75°F (demo response)"
            
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return f"The weather in {city} is {description} with a temperature of {temp}°C"
            else:
                return f"Could not get weather for {city}"
                
        except Exception as e:
            return f"Error getting weather: {e}"
'''

example_math_plugin = '''
import math
import re
from vecna_plugin_system import VecnaPlugin

class MathPlugin(VecnaPlugin):
    def __init__(self):
        super().__init__(
            name="Math",
            description="Perform mathematical calculations",
            version="1.0"
        )
    
    def get_commands(self):
        return ["calculate", "math", "solve", "what is"]
    
    def execute(self, command, context):
        try:
            # Extract mathematical expression
            expression = command.lower()
            
            # Remove command words
            for cmd in ["calculate", "math", "solve", "what is", "what's"]:
                expression = expression.replace(cmd, "")
            
            expression = expression.strip()
            
            # Replace word numbers and operators
            replacements = {
                "plus": "+", "add": "+", "and": "+",
                "minus": "-", "subtract": "-",
                "times": "*", "multiply": "*", "multiplied by": "*",
                "divided by": "/", "divide": "/",
                "squared": "**2", "cubed": "**3",
                "square root of": "math.sqrt(",
                "sin": "math.sin(", "cos": "math.cos(", "tan": "math.tan("
            }
            
            for word, symbol in replacements.items():
                expression = expression.replace(word, symbol)
            
            # Count parentheses for square root
            if "math.sqrt(" in expression:
                expression += ")" * expression.count("math.sqrt(")
            
            # Evaluate safely
            allowed_names = {
                "math": math,
                "__builtins__": {},
            }
            
            result = eval(expression, allowed_names)
            return f"The answer is {result}"
            
        except Exception as e:
            return f"Could not calculate that. Please try a simpler expression. Error: {e}"
'''

example_todo_plugin = '''
import json
import os
from datetime import datetime
from vecna_plugin_system import VecnaPlugin

class TodoPlugin(VecnaPlugin):
    def __init__(self):
        super().__init__(
            name="Todo",
            description="Manage your todo list",
            version="1.0"
        )
        self.todo_file = "vecna_todos.json"
        self.load_todos()
    
    def get_commands(self):
        return ["add todo", "add task", "todo", "task", "remove todo", "list todos", "clear todos"]
    
    def load_todos(self):
        try:
            if os.path.exists(self.todo_file):
                with open(self.todo_file, 'r') as f:
                    self.todos = json.load(f)
            else:
                self.todos = []
        except:
            self.todos = []
    
    def save_todos(self):
        with open(self.todo_file, 'w') as f:
            json.dump(self.todos, f, indent=2)
    
    def execute(self, command, context):
        command_lower = command.lower()
        
        if "add todo" in command_lower or "add task" in command_lower:
            # Extract todo text
            for phrase in ["add todo", "add task"]:
                if phrase in command_lower:
                    todo_text = command[command_lower.find(phrase) + len(phrase):].strip()
                    break
            
            if todo_text:
                todo = {
                    "text": todo_text,
                    "created": datetime.now().isoformat(),
                    "completed": False
                }
                self.todos.append(todo)
                self.save_todos()
                return f"Added todo: {todo_text}"
            else:
                return "Please specify what to add to your todo list"
        
        elif "remove todo" in command_lower:
            # Remove by index or text matching
            todo_text = command[command_lower.find("remove todo") + len("remove todo"):].strip()
            
            # Try to find matching todo
            for i, todo in enumerate(self.todos):
                if todo_text.lower() in todo["text"].lower():
                    removed_todo = self.todos.pop(i)
                    self.save_todos()
                    return f"Removed todo: {removed_todo['text']}"
            
            return f"Could not find todo containing '{todo_text}'"
        
        elif "list todos" in command_lower or command_lower.strip() == "todo":
            if not self.todos:
                return "Your todo list is empty"
            
            todo_list = "Your todos:\\n"
            for i, todo in enumerate(self.todos, 1):
                status = "✓" if todo["completed"] else "○"
                todo_list += f"{i}. {status} {todo['text']}\\n"
            
            return todo_list
        
        elif "clear todos" in command_lower:
            self.todos = []
            self.save_todos()
            return "Cleared all todos"
        
        return "Todo command not recognized"
'''

# Create example plugins
def create_example_plugins():
    """Create example plugin files"""
    plugins_dir = "plugins"
    if not os.path.exists(plugins_dir):
        os.makedirs(plugins_dir)
    
    # Write example plugins
    with open(os.path.join(plugins_dir, "weather_plugin.py"), "w") as f:
        f.write(example_weather_plugin)
    
    with open(os.path.join(plugins_dir, "math_plugin.py"), "w") as f:
        f.write(example_math_plugin)
    
    with open(os.path.join(plugins_dir, "todo_plugin.py"), "w") as f:
        f.write(example_todo_plugin)
    
    print("Created example plugins in the plugins directory")

if __name__ == "__main__":
    # Create example plugins
    create_example_plugins()
    
    # Test the plugin system
    pm = PluginManager()
    print("Available commands:", pm.get_all_commands())
    
    # Test some commands
    test_commands = [
        "add todo buy groceries",
        "list todos",
        "calculate 15 plus 25",
        "weather in Paris"
    ]
    
    for cmd in test_commands:
        result = pm.execute_plugin_command(cmd, {})
        print(f"Command: {cmd}")
        print(f"Result: {result}\\n")
