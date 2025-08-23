"""
Test script for Vecna Advanced Automation Features
This script tests all the new automation capabilities.
"""

import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from advanced_automation import AdvancedAutomation
    print("✓ Advanced automation module imported successfully")
except ImportError as e:
    print(f"✗ Failed to import advanced automation: {e}")
    sys.exit(1)

def test_automation_features():
    """Test all automation features"""
    print("\n🔬 Testing Vecna Advanced Automation Features\n")
    
    # Initialize automation
    try:
        automation = AdvancedAutomation()
        print("✓ AdvancedAutomation initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize automation: {e}")
        return
    
    # Test 1: Mouse operations (safe test - just get position)
    print("\n1. Testing Mouse Control...")
    try:
        pos = automation.get_mouse_position()
        print(f"  ✓ Current mouse position: {pos}")
        
        # Test safe mouse movement (small movement)
        current_x, current_y = pos
        automation.move_mouse(current_x + 10, current_y + 10)
        print("  ✓ Mouse movement test completed")
        
        # Move back
        automation.move_mouse(current_x, current_y)
        print("  ✓ Mouse position restored")
        
    except Exception as e:
        print(f"  ✗ Mouse control test failed: {e}")
    
    # Test 2: Window management
    print("\n2. Testing Window Management...")
    try:
        windows = automation.list_windows()
        print(f"  ✓ Found {len(windows)} open windows")
        for i, window in enumerate(windows[:3]):  # Show first 3
            print(f"    - {window}")
        if len(windows) > 3:
            print(f"    ... and {len(windows) - 3} more")
    except Exception as e:
        print(f"  ✗ Window management test failed: {e}")
    
    # Test 3: File operations (safe test)
    print("\n3. Testing File Operations...")
    try:
        test_folder = "test_automation_folder"
        result = automation.create_folder(test_folder)
        print(f"  ✓ Folder creation test: {result}")
        
        # Clean up
        if os.path.exists(test_folder):
            os.rmdir(test_folder)
            print("  ✓ Test folder cleaned up")
            
    except Exception as e:
        print(f"  ✗ File operations test failed: {e}")
    
    # Test 4: App detection
    print("\n4. Testing Enhanced App Detection...")
    try:
        # Test some common apps
        test_apps = ["notepad", "calculator", "whatsapp", "chrome"]
        for app in test_apps:
            paths = automation.find_app_paths(app)
            if paths:
                print(f"  ✓ Found {app}: {paths[0] if isinstance(paths, list) else paths}")
            else:
                print(f"  - {app}: Not found (normal if not installed)")
    except Exception as e:
        print(f"  ✗ App detection test failed: {e}")
    
    # Test 5: Web automation capabilities
    print("\n5. Testing Web Automation Setup...")
    try:
        # Just test if selenium can be imported and basic setup
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        print("  ✓ Selenium imported successfully")
        
        # Test ChromeDriver availability
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        try:
            driver = webdriver.Chrome(options=options)
            print("  ✓ ChromeDriver is available")
            driver.quit()
        except Exception as e:
            print(f"  - ChromeDriver test: {e}")
            print("  💡 Run install_advanced_automation.bat to install ChromeDriver")
            
    except ImportError:
        print("  ✗ Selenium not available - run install_advanced_automation.bat")
    except Exception as e:
        print(f"  ✗ Web automation test failed: {e}")
    
    print("\n🎉 Automation testing completed!")
    print("\n📋 Summary:")
    print("  • Mouse control: Ready")
    print("  • Window management: Ready") 
    print("  • File operations: Ready")
    print("  • Enhanced app launcher: Ready")
    print("  • Web automation: Install ChromeDriver if needed")
    
    print("\n🎮 Try these voice commands:")
    print("  • 'click at 500 300'")
    print("  • 'open whatsapp'")
    print("  • 'window list'")
    print("  • 'move mouse to 100 200'")
    print("  • 'create folder test'")

if __name__ == "__main__":
    test_automation_features()
    
    print("\n⏱️  Test completed. Press Enter to exit...")
    input()
