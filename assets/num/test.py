import time
import numpy as np
import cv2
import mss
import numpy as np
import cv2
import mss

basePATH = './'  # Ensure this path is correct and contains your template images

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


hp_region = [599, 1317, 63, 35]

while True:
    start = time.time()
    res = detect_numbers(hp_region)
    print(res)
    print(time.time()-start)