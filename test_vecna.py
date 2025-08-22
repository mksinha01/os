"""
Test script for Enhanced Vecna Voice Assistant
Runs basic tests to ensure all components are working
"""

import os
import sys
import importlib
import json

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    required_modules = [
        'speech_recognition',
        'pyttsx3',
        'pyautogui',
        'pyperclip',
        'keyboard',
        'requests',
        'psutil'
    ]
    
    optional_modules = [
        'openai',
        'google.generativeai',
        'whisper',
        'tkinter',
        'PIL',
        'plyer',
        'win32gui'
    ]
    
    success_count = 0
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}")
            success_count += 1
        except ImportError as e:
            print(f"✗ {module} - {e}")
    
    print(f"\nRequired modules: {success_count}/{len(required_modules)} working")
    
    optional_success = 0
    for module in optional_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module} (optional)")
            optional_success += 1
        except ImportError:
            print(f"- {module} (optional) - not installed")
    
    print(f"Optional modules: {optional_success}/{len(optional_modules)} working")
    
    return success_count == len(required_modules)

def test_files():
    """Test if all required files exist"""
    print("\nTesting files...")
    
    required_files = [
        'vecna.py',
        'vecna_enhanced.py',
        'vecna_simple.py',
        'config.json'
    ]
    
    optional_files = [
        'vecna_gui.py',
        'vecna_plugin_system.py',
        'advanced_system_control.py',
        'requirements_complete.txt'
    ]
    
    success_count = 0
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
            success_count += 1
        else:
            print(f"✗ {file} - missing")
    
    for file in optional_files:
        if os.path.exists(file):
            print(f"✓ {file} (optional)")
        else:
            print(f"- {file} (optional) - missing")
    
    return success_count == len(required_files)

def test_config():
    """Test configuration file"""
    print("\nTesting configuration...")
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        required_sections = [
            'speech_recognition',
            'text_to_speech',
            'ai_integration',
            'gui',
            'system_control'
        ]
        
        for section in required_sections:
            if section in config:
                print(f"✓ {section} section")
            else:
                print(f"✗ {section} section missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_basic_functionality():
    """Test basic Vecna functionality"""
    print("\nTesting basic functionality...")
    
    try:
        # Test basic imports
        from vecna import Config, SpeechEngine, SpeechRecognizer
        print("✓ Core classes importable")
        
        # Test configuration
        config = Config()
        print("✓ Configuration loading")
        
        # Test text-to-speech (without speaking)
        speech_engine = SpeechEngine()
        print("✓ Text-to-speech engine")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality error: {e}")
        return False

def test_enhanced_features():
    """Test enhanced features if available"""
    print("\nTesting enhanced features...")
    
    try:
        # Test plugin system
        if os.path.exists('vecna_plugin_system.py'):
            from vecna_plugin_system import PluginManager
            plugin_manager = PluginManager()
            print("✓ Plugin system")
        else:
            print("- Plugin system not available")
        
        # Test advanced system control
        if os.path.exists('advanced_system_control.py'):
            from advanced_system_control import AdvancedSystemController
            controller = AdvancedSystemController()
            print("✓ Advanced system control")
        else:
            print("- Advanced system control not available")
        
        # Test GUI
        try:
            if os.path.exists('vecna_gui.py'):
                import tkinter
                print("✓ GUI components available")
            else:
                print("- GUI not available")
        except ImportError:
            print("- GUI not available (tkinter missing)")
        
        return True
    except Exception as e:
        print(f"✗ Enhanced features error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("VECNA VOICE ASSISTANT - SYSTEM TEST")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("File Test", test_files),
        ("Configuration Test", test_config),
        ("Basic Functionality Test", test_basic_functionality),
        ("Enhanced Features Test", test_enhanced_features)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! Vecna is ready to use.")
        print("Run 'start_vecna.bat' to launch the assistant.")
    elif passed >= 3:
        print("\n⚠️ Most tests passed. Vecna should work with basic features.")
        print("Some advanced features may not be available.")
    else:
        print("\n❌ Several tests failed. Please check the requirements and setup.")
        print("Try running 'pip install -r requirements_complete.txt'")

if __name__ == "__main__":
    run_all_tests()
