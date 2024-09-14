from pynput.mouse import Listener
import mss
from PIL import Image
import pytesseract
import pyperclip

start_pos = None
end_pos = None

# Set the tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to capture the mouse click down (start position)
def on_click(x, y, button, pressed):
    global start_pos, end_pos

    if pressed:  # Mouse button pressed down
        start_pos = (x, y)
        print(f"Mouse pressed at: {start_pos}")
    else:  # Mouse button released
        end_pos = (x, y)
        print(f"Mouse released at: {end_pos}")
        # Stop listener after getting the end position
        return False


count=0
# Start listener to track mouse events
while True:
    with Listener(on_click=on_click) as listener:
        listener.join()
    if start_pos and end_pos:
        left = min(start_pos[0], end_pos[0])
        top = min(start_pos[1], end_pos[1])
        width = abs(start_pos[0] - end_pos[0])
        height = abs(start_pos[1] - end_pos[1])
        mn=abs(width*height)
        if mn<20000:
            continue
        with mss.mss() as sct:
            monitor = {"top": top, "left": left, "width": width, "height": height}
            screenshot = sct.grab(monitor)
            # Convert to a Pillow image
            img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
            # Save the screenshot
            file_name="".join(["captured_part",str(count),".png"])
            text = pytesseract.image_to_string(img)
            img.save(file_name)
            count+=1
            pyperclip.copy(text)
            print(text)






