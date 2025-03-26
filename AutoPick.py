import pydirectinput
import time
import win32gui
import win32con
import cv2
import numpy as np
import threading
import keyboard
import mss

# ---------- Config ----------
BAR_REGION = (950, 650, 650, 100)  # (left, top, width, height)
debug_enabled = True  # Set to True to see what the bot sees

# HSV color ranges
GREEN_LOWER = np.array([40, 80, 80])
GREEN_UPPER = np.array([90, 255, 255])
WHITE_LOWER = np.array([0, 0, 200])
WHITE_UPPER = np.array([180, 30, 255])

# Global toggle state
auto_pick_enabled = False

# ---------- Focus Game Window ----------
def focus_game_window(title="Schedule I"):
    game_window = win32gui.FindWindow(None, title)
    if game_window:
        try:
            win32gui.ShowWindow(game_window, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(game_window)
            print("Game window focused programmatically.")
        except Exception as e:
            print(f"Error focusing window: {e}. Please focus manually.")
            input("Focus the game window now, then press Enter.")
    else:
        print(f"Could not find '{title}'. Please focus it manually, then press Enter.")
        input()

    time.sleep(1)
    if win32gui.GetForegroundWindow() == game_window:
        print("Focus confirmed.")
    else:
        print("Focus not confirmed. Ensure the game is active.")

# ---------- Press Space (pydirectinput) ----------
def press_space():
    pydirectinput.keyDown('space')
    time.sleep(0.3)  # Reduced from 0.5 to make it more responsive
    pydirectinput.keyUp('space')
    print("✅ SPACE held for 300ms")

# ---------- Visual Detection ----------
def find_arrow_and_green_bar(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
    white_mask = cv2.inRange(hsv, WHITE_LOWER, WHITE_UPPER)

    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    white_contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    green_x1 = green_x2 = arrow_x = None
    green_box = arrow_box = None

    if green_contours:
        largest = max(green_contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        green_x1, green_x2 = x, x + w
        green_box = (x, y, w, h)

    if white_contours:
        largest = max(white_contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        arrow_x = x + w // 2
        arrow_box = (x, y, w, h)

    return green_x1, green_x2, arrow_x, green_box, arrow_box

# ---------- Auto Pick Thread with MSS ----------
def auto_pick_loop():
    global auto_pick_enabled
    print("AutoPick loop started. Press CTRL + ALT to toggle.")
    monitor = {"top": BAR_REGION[1], "left": BAR_REGION[0], "width": BAR_REGION[2], "height": BAR_REGION[3]}
    with mss.mss() as sct:
        while True:
            if auto_pick_enabled:
                sct_img = sct.grab(monitor)
                frame = np.array(sct_img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                green_x1, green_x2, arrow_x, green_box, arrow_box = find_arrow_and_green_bar(frame)

                if green_box:
                    x, y, w, h = green_box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if arrow_box:
                    x, y, w, h = arrow_box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

                if green_x1 and green_x2 and arrow_x:
                    if green_x1 <= arrow_x <= green_x2:
                        press_space()
                        time.sleep(0.3)

                if debug_enabled:
                    cv2.imshow("DEBUG - Detection Region", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break

            time.sleep(0.005)

# ---------- Toggle Hotkey ----------
def toggle_listener():
    global auto_pick_enabled
    print("Press CTRL + ALT to start/stop AutoPick.")
    while True:
        keyboard.wait('ctrl+alt')
        auto_pick_enabled = not auto_pick_enabled
        state = "ENABLED" if auto_pick_enabled else "DISABLED"
        print(f"AutoPick {state}")
        time.sleep(0.5)

# ---------- Run ----------
if __name__ == "__main__":
    focus_game_window()

    threading.Thread(target=auto_pick_loop, daemon=True).start()
    toggle_listener()