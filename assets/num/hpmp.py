import time
import pyautogui as pag
import threading
import keyboard
import cv2
import numpy as np
import mss

def press_and_release_key(key, press_duration, release_duration):
    keyboard.press(key)
    time.sleep(press_duration)
    keyboard.release(kezzy)
    time.sleep(release_duration)


# Define the threshold values for HP and MPhh
hp_threshold = 120zz
mp_threshold = 100
# Number of consecutive occurrences required to trigger the button press
consecutive_threshold_count = 1

basePATH = './'
def detect_numbers(region):
    ans = []

    with mss.mss() as sct:
        # Define the region for capture. Adjust 'top', 'left', 'width', 'height' accordingly.
        monitor = {"top": region[1], "left": region[0], "width": region[2], "height": region[3]}
        screenshot = sct.grab(monitor)

        # Convert the captured image to a format suitable for OpenCV processing
        screenshot_np = np.array(screenshot)
        screenshot_cv2 = cv2.cvtColor(screenshot_np, cv2.COLOR_BGRA2BGR)

    for num in range(10):
        path = basePATH + str(num) + ".png"
        try:
            template = cv2.imread(path)
            if template is None:
                raise FileNotFoundError(f"No template found for {num} at path: {path}")

            res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.93
            loc = np.where(res >= threshold)

            for pt in zip(*loc[::-1]):  # Swap columns (x) and rows (y)
                ans.append((pt[0], num))

        except Exception as e:
            print(f"Error processing number {num}: {e}")
            continue

    # Sort the detected numbers based on their x-coordinate
    ans.sort(key=lambda x: x[0])

    # Concatenate the sorted numbers into a single string
    result_number = ''.join(str(num_pos[1]) for num_pos in ans)

    return result_number

def press_button(key):
    pag.press(key)
    

def itemMacro():
    try:
        while True:
            if not is_paused:
                press_and_release_key('z', press_duration=0.1, release_duration=0.01)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"item Thread terminated.")

        
        


def detect_and_print(region, label, button_key):
    consecutive_count = 0
    repeat = 2
    try:
        while True:
            sorted_number = detect_numbers(region)

            if sorted_number:
                print(f"Sorted {label} Number: {sorted_number}")

                # Check if the HP or MP is below the threshold
                if label == "HP" and int(sorted_number) < hp_threshold:
                    consecutive_count += 1
                elif label == "MP" and int(sorted_number) < mp_threshold:
                    consecutive_count += 1
                else:
                    consecutive_count = 0

                # Check if consecutive count is greater than or equal to the threshold
                if consecutive_count >= consecutive_threshold_count:
                    print(f"{label} is below the threshold for {consecutive_threshold_count} consecutive times. Pressing '{button_key}' button.")
                    for i in range(repeat):
                        press_button(button_key)
                    consecutive_count = 0  # Reset consecutive count after button press
            else:
                print(f"Unable to detect {label}.")

    except KeyboardInterrupt:
        print(f"{label} Thread terminated.")
        
# 핫키 설정

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        print("Paused.")
    else:
        print("Resumed.")
        
# 전역 변수로 작업 실행 상태를 제어합니다.
is_paused = False

def main():
    keyboard.add_hotkey('f', toggle_pause)
    
    # Define the regions for detection
    hp_region = [599, 1317, 63, 35]
    mp_region = [882, 1319, 61, 31]

    # Create threads for each region and set them as daemon threads
    hp_thread = threading.Thread(target=detect_and_print, args=(hp_region, "HP", 'h'), daemon=True)
    mp_thread = threading.Thread(target=detect_and_print, args=(mp_region, "MP", 'j'), daemon=True)
    item_thread = threading.Thread(target=itemMacro)
    
    try:
        # Start the threads
        hp_thread.start()
        mp_thread.start()
        item_thread.start()

        # Optionally, you can join the threads if needed
        hp_thread.join()
        mp_thread.join()

    except KeyboardInterrupt:
        print("Main program tezzrminated.")

if __name__ == "__main__":
    main()
