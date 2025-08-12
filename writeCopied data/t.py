import pyautogui
import pyperclip
import time

# Wait a few seconds to let you focus on the target window
time.sleep(4)

# Get text from clipboard
copied_text = pyperclip.paste()

# Type the copied text
pyautogui.write(copied_text, interval=0)  # 0.05 sec delay between characters
