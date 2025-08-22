"""
Quick test script to verify Vecna fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vecna import CommandProcessor, SystemController, SpeechEngine, Memory, Intelligence

def test_commands():
    print("Testing Vecna command processing...")
    
    # Initialize components
    speech_engine = SpeechEngine()
    system = SystemController()
    memory = Memory()
    intelligence = Intelligence(memory)
    
    # Create command processor
    processor = CommandProcessor(speech_engine, system, memory, intelligence)
    
    # Test commands
    test_cases = [
        "take screenshot",
        "what time is it",
        "system info", 
        "screenshot",
        "time",
        "joke",
        "volume up",
        "volume down"
    ]
    
    print("\nTesting commands:")
    print("=" * 50)
    
    for command in test_cases:
        try:
            response, action = processor.process_command(command)
            print(f"✓ '{command}' -> {response}")
        except Exception as e:
            print(f"✗ '{command}' -> ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("Test complete!")

if __name__ == "__main__":
    test_commands()
