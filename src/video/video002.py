
# capture video from camera
# Frame Differencing - save only if changes happen

    # 1. Convert to Grayscale: Color doesn't matter for motion, and grayscale is faster to process.
    # 2. Apply Gaussian Blur: This smooths out the image and eliminates tiny, random camera noise.
    # 3. Calculate the Absolute Difference: We subtract the previous frame from the current frame.
    # 4. Apply a Threshold: We tell the script, "If a pixel changed by more than X amount, consider it a real change."
    # 5. Count the Changes: If enough pixels changed, we write the frame to the video file.
    # 6. The "Cooldown" Buffer. adding a timer, you can tell OpenCV: "If you see motion, keep recording for at least 2 more seconds even if things go quiet."

import cv2
import datetime
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Error opening video stream or file')
    exit()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# WINDOWS -- *'DIVX' | LINUX -- *'XVID'
writer = cv2.VideoWriter('output/myvideo001.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width, height))

# 1. Read the very first frame to establish our starting baseline
ret, prev_frame = cap.read()
if not ret:
    print("Failed to grab initial frame.")
    exit()

# Convert the baseline frame to grayscale and blur it
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

# --- SENSITIVITY SETTINGS ---
# Adjust this number based on your camera resolution.
# Higher = requires MORE movement to trigger recording.
MOTION_THRESHOLD = 5000

# "Cooldown"
last_motion_time = 0
buffer_seconds = 2  # Keep recording for 2 seconds after motion stops

print("Starting motion detection... Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 2. Process the current frame (Grayscale + Blur)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # 3. Compute the absolute difference between the previous frame and current frame
    frame_diff = cv2.absdiff(prev_gray, gray)

    # 4. Apply a threshold (pixels with a difference > 25 become white, rest become black)
    _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

    # 5. Count the "changed" (white) pixels
    changed_pixels = cv2.countNonZero(thresh)

    # 6. If the amount of change exceeds our threshold, write the original colored frame!
    # if changed_pixels > MOTION_THRESHOLD:
    #     print(f"Motion detected! Changed pixels: {changed_pixels}") # Uncomment to debug
    #     writer.write(frame)

    motion_detected = changed_pixels > MOTION_THRESHOLD

    if motion_detected:
        last_motion_time = time.time()  # Reset the timer

    # Check if we are within the "Motion Window" or the "Cooldown Window"
    if motion_detected or (time.time() - last_motion_time < buffer_seconds):
        # Add a Timestamp to the frame
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, height - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        writer.write(frame)


    # Show the video feed
    cv2.imshow('Frame', frame)

    # Optional: Show the black & white difference mask to help you calibrate the MOTION_THRESHOLD
    cv2.imshow('Motion Mask', thresh)

    # 7. VERY IMPORTANT: Update the previous frame so we can compare it to the next one
    prev_gray = gray

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
writer.release()
cv2.destroyAllWindows()
