import sys
import time
import os

# Ensure local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import speech_recognition as sr
except Exception as e:
    print("SpeechRecognition import error:", e)
    sys.exit(1)

try:
    from vecna_bridge import create_vecna_bridge
except Exception as e:
    print("Vecna bridge import error:", e)
    sys.exit(1)

print("=== Microphone Devices ===")
try:
    names = sr.Microphone.list_microphone_names()
    for i, name in enumerate(names):
        print(f"{i}: {name}")
except Exception as e:
    print("Mic enumeration error:", e)
    names = []

# Auto-pick a mic index
mic_index = None
if names:
    # Prefer a device name with 'microphone' in it, else index 0
    preferred = next((i for i, n in enumerate(names) if 'microphone' in (n or '').lower()), None)
    mic_index = preferred if preferred is not None else 0

# Allow override via CLI arg
if len(sys.argv) > 1:
    try:
        mic_index = int(sys.argv[1])
    except Exception:
        pass

print(f"Selected mic index: {mic_index}")

b = create_vecna_bridge(lambda s, m: print(f"[{s}] {m}"))
print("Initializing backend...")
if not b.initialize():
    print("Backend failed to initialize.")
    sys.exit(2)

# Apply options: no-wake-word and mic device
try:
    b.set_no_wake_word(True)
    if mic_index is not None:
        b.set_mic_index(mic_index)
except Exception as e:
    print("Setting options failed:", e)

print("Starting listening for ~8 seconds (no wake word)...")
started = b.start_listening()
print("Started:", started)

# Wait a bit to allow speaking a test command
try:
    time.sleep(8)
finally:
    print("Stopping listening...")
    b.stop_listening()

print("Done.")
