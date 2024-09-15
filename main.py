import pytesseract
import pyperclip

start_pos = None
end_pos = None

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from pynput import mouse, keyboard
import mss
from PIL import Image

# Variables to store the starting and ending positions of the mouse drag
start_pos = None
end_pos = None
is_left_button_pressed = False
is_ctrl_pressed = False


# Function to handle keyboard press events (for detecting Ctrl)
def on_key_press(key):
    global is_ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        is_ctrl_pressed = True



# Function to handle keyboard release events (for detecting Ctrl release)
def on_key_release(key):
    global is_ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        is_ctrl_pressed = False



# Function to handle mouse click events
def on_click(x, y, button, pressed):
    global start_pos, end_pos, is_left_button_pressed, is_ctrl_pressed


    # Only proceed if the Ctrl key is held down
    if is_ctrl_pressed and button == mouse.Button.left:
        if pressed:  # Left button pressed down
            is_left_button_pressed = True
            start_pos = (x, y)  # Store the start position
            print(f"Mouse pressed at: {start_pos} with Ctrl pressed")

        else:  # Left button released
            is_left_button_pressed = False
            end_pos = (x, y)  # Store the end position
            print(f"Mouse released at: {end_pos} with Ctrl pressed")

            # Capture the screen region after the left button is released
            capture_screen_region(start_pos, end_pos)




# Function to capture the selected region of the screen
def capture_screen_region(start, end):
    left = min(start[0], end[0])
    top = min(start[1], end[1])
    width = abs(start[0] - end[0])
    height = abs(start[1] - end[1])
    sq = abs(width * height)
    if sq<2000:
        return
    print(f" sq={sq} width={width} height={height}")
    # Use mss to capture the defined screen region
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        # Convert the screenshot to a Pillow image
        img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
        file_name="".join(["captured_part",str(sq),".png"])
        text = pytesseract.image_to_string(img)

        pyperclip.copy(text)
        print(text)



# Set up listeners for both keyboard (Ctrl detection) and mouse (click detection)
keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
mouse_listener = mouse.Listener(on_click=on_click)

# Start the listeners
keyboard_listener.start()
mouse_listener.start()

# Keep the program running to listen for events
keyboard_listener.join()
mouse_listener.join()




