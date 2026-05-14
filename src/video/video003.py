
# capture video from camera
# Frame Differencing - save only if changes happen

    # 1. Convert to Grayscale: Color doesn't matter for motion, and grayscale is faster to process.
    # 2. Apply Gaussian Blur: This smooths out the image and eliminates tiny, random camera noise.
    # 3. Calculate the Absolute Difference: We subtract the previous frame from the current frame.
    # 4. Apply a Threshold: We tell the script, "If a pixel changed by more than X amount, consider it a real change."
    # 5. Count the Changes: If enough pixels changed, we write the frame to the video file.
    # 6. The "Cooldown" Buffer. adding a timer, you can tell OpenCV: "If you see motion, keep recording for at least 2 more seconds even if things go quiet."

# Adding classifier

    # The Pipeline
    # Background Subtraction: OpenCV isolates the moving object (e.g., the cat) and makes the rest of the room completely black.
    # Base64 Encoding: We convert that masked image into a text string.
    # The API Call: We send that string to LM Studio's local server (usually running on port 1234) just like we would to OpenAI.


# Motion happens.
    #
    # The if statement triggers.
    #
    # Python spins up a background thread using threading.Thread().
    #
    # The background thread takes the image and goes to talk to LM Studio.
    #
    # Crucially: The main while cap.isOpened(): loop immediately continues to the next frame. The video window never freezes!
    #
    # You will see the red text "AI THINKING..." on your live video feed until the background thread finishes, at which point the text updates to whatever Gemma 4 saw.
    #

import cv2
import base64
import requests
import threading
import time

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
'http://127.0.0.1:1234/api/v1/chat'

MODEL_NAME = "gemma-4-e4b"

# --- STATE VARIABLES ---
is_ai_thinking = False
last_ai_result = "Waiting for motion..."


def background_ai_task(image_frame):
    """This runs in a separate thread! It will not freeze the camera."""
    global is_ai_thinking, last_ai_result

    is_ai_thinking = True
    print("🧠 AI thread started. Sending image to Gemma 4...")

    try:
        # Encode image
        _, buffer = cv2.imencode('.jpg', image_frame)
        base64_image = base64.b64encode(buffer).decode('utf-8')

        # Build payload
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What is the main moving object? Keep it brief."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            "max_tokens": 50,
            "temperature": 0.3
        }

        # Send request (The thread "sleeps" here, letting OpenCV run)
        response = requests.post(LM_STUDIO_URL, json=payload)
        result = response.json()

        last_ai_result = result['choices'][0]['message']['content'].strip()
        print(f"✅ AI finished! Result: {last_ai_result}")

    except Exception as e:
        last_ai_result = f"Error: {e}"
        print(last_ai_result)

    finally:
        is_ai_thinking = False  # Unlock so we can trigger again later


# --- MAIN OPENCV LOOP ---

cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    fgmask = fgbg.apply(frame)
    fgmask = cv2.medianBlur(fgmask, 5)
    motion_pixels = cv2.countNonZero(fgmask)
    foreground_only = cv2.bitwise_and(frame, frame, mask=fgmask)

    # TRIGGER CONDITION: Lots of motion AND the AI isn't currently busy
    if motion_pixels > 8000 and not is_ai_thinking:
        # We copy the frame so the thread has its own safe version to encode
        frame_to_send = foreground_only.copy()

        # 🚀 START THE THREAD!
        ai_thread = threading.Thread(target=background_ai_task, args=(frame_to_send,))
        ai_thread.daemon = True  # This ensures the thread dies when the main program closes
        ai_thread.start()

    # --- DISPLAY LOGIC ---
    # We can draw the AI's last result directly onto the live feed!
    status_text = "AI THINKING..." if is_ai_thinking else f"Last Seen: {last_ai_result}"
    color = (0, 0, 255) if is_ai_thinking else (0, 255, 0)

    cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow('Live Camera (Unfrozen)', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# import cv2
# import base64
# import requests
# import time
#
# # --- CONFIGURATION ---
# LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
# # Make sure this matches the exact model name loaded in LM Studio
# MODEL_NAME = "gemma-4-e4b"  # or whatever specific Gemma 4 variant you are running
#
#
# def ask_gemma_what_this_is(image_frame):
#     """Encodes the frame and sends it to LM Studio's local API."""
#     # 1. Convert the OpenCV image (NumPy array) to a JPEG
#     _, buffer = cv2.imencode('.jpg', image_frame)
#     # 2. Encode to Base64
#     base64_image = base64.b64encode(buffer).decode('utf-8')
#
#     # 3. Construct the OpenAI-compatible payload for LM Studio
#     payload = {
#         "model": MODEL_NAME,
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": "This image has the background removed. What is the main moving object in this image? Reply with just a few words."
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             # Note: Some LM Studio versions just want the raw base64 string,
#                             # but the standard data URI is generally preferred.
#                             "url": f"data:image/jpeg;base64,{base64_image}"
#                         }
#                     }
#                 ]
#             }
#         ],
#         "max_tokens": 50,
#         "temperature": 0.3  # Low temperature for more factual identification
#     }
#
#     try:
#         response = requests.post(LM_STUDIO_URL, json=payload)
#         result = response.json()
#         return result['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         return f"API Error: {e}"
#
#
# # --- MAIN OPENCV LOOP ---
#
# cap = cv2.VideoCapture(0)
#
# # Create the Background Subtractor object
# # history: How many previous frames it remembers to model the background
# # varThreshold: Sensitivity to changes
# fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)
#
# last_api_call = 0
# COOLDOWN_SECONDS = 10  # Wait 10 seconds between AI requests so we don't spam LM Studio
#
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret: break
#
#     # 1. Apply the background subtractor to get the foreground mask (White = Motion, Black = Static)
#     fgmask = fgbg.apply(frame)
#
#     # Clean up the mask slightly (remove tiny noise)
#     fgmask = cv2.medianBlur(fgmask, 5)
#
#     # Count the moving pixels
#     motion_pixels = cv2.countNonZero(fgmask)
#
#     # 2. Apply the mask to the ORIGINAL frame using bitwise_and
#     # This keeps the original colors of the moving object, but makes the background black
#     foreground_only = cv2.bitwise_and(frame, frame, mask=fgmask)
#
#     # 3. If there is significant motion, AND we aren't cooling down, trigger the AI!
#     current_time = time.time()
#     if motion_pixels > 8000 and (current_time - last_api_call > COOLDOWN_SECONDS):
#         print("Significant motion detected! Passing to Gemma 4...")
#
#         # We pass the 'foreground_only' image to the AI, not the full frame
#         ai_response = ask_gemma_what_this_is(foreground_only)
#
#         print(f"🤖 Gemma 4 says: {ai_response}")
#         last_api_call = current_time
#
#     # Display the results
#     cv2.imshow('Original Frame', frame)
#     cv2.imshow('Minus Background (Sent to AI)', foreground_only)
#
#     if cv2.waitKey(20) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
#
# #
# # import cv2
# # import datetime
# # import time
# # from ultralytics import YOLO
# # import base64
# #
# # cap = cv2.VideoCapture(0)
# #
# # if not cap.isOpened():
# #     print('Error opening video stream or file')
# #     exit()
# #
# # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# #
# # # WINDOWS -- *'DIVX' | LINUX -- *'XVID'
# # writer = cv2.VideoWriter('myvideo001.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width, height))
# #
# # # 1. Read the very first frame to establish our starting baseline
# # ret, prev_frame = cap.read()
# # if not ret:
# #     print("Failed to grab initial frame.")
# #     exit()
# #
# # # Convert the baseline frame to grayscale and blur it
# # prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
# # prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)
# #
# # # --- SENSITIVITY SETTINGS ---
# # # Adjust this number based on your camera resolution.
# # # Higher = requires MORE movement to trigger recording.
# # MOTION_THRESHOLD = 5000
# #
# # # "Cooldown"
# # last_motion_time = 0
# # buffer_seconds = 2  # Keep recording for 2 seconds after motion stops
# #
# # # Load the pre-trained AI model (it downloads automatically the first time)
# # model = YOLO('yolov8n.pt') # 'n' stands for nano - very fast and lightweight!
# #
# # print("Starting motion detection... Press 'q' to quit.")
# #
# # while cap.isOpened():
# #     ret, frame = cap.read()
# #     if not ret:
# #         break
# #
# #     # 2. Process the current frame (Grayscale + Blur)
# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# #     gray = cv2.GaussianBlur(gray, (21, 21), 0)
# #
# #     # 3. Compute the absolute difference between the previous frame and current frame
# #     frame_diff = cv2.absdiff(prev_gray, gray)
# #
# #     # 4. Apply a threshold (pixels with a difference > 25 become white, rest become black)
# #     _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
# #
# #     # 5. Count the "changed" (white) pixels
# #     changed_pixels = cv2.countNonZero(thresh)
# #
# #     # 6. If the amount of change exceeds our threshold, write the original colored frame!
# #     # if changed_pixels > MOTION_THRESHOLD:
# #     #     print(f"Motion detected! Changed pixels: {changed_pixels}") # Uncomment to debug
# #     #     writer.write(frame)
# #
# #     motion_detected = changed_pixels > MOTION_THRESHOLD
# #
# #     if motion_detected:
# #         last_motion_time = time.time()  # Reset the timer
# #
# #     # Check if we are within the "Motion Window" or the "Cooldown Window"
# #     if motion_detected or (time.time() - last_motion_time < buffer_seconds):
# #         # Add a Timestamp to the frame
# #         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #         cv2.putText(frame, timestamp, (10, height - 10),
# #                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
# #
# #         results = model(frame)
# #         # The AI returns a list of everything it found
# #         for result in results:
# #             for box in result.boxes:
# #                 class_id = int(box.cls[0])
# #                 label = model.names[class_id]  # e.g., "person", "dog", "cat"
# #                 confidence = box.conf[0]
# #
# #                 if label in ["person", "dog", "cat"] and confidence > 0.60:
# #                     print(f"ALERT: I see a {label}!")
# #                     # Draw a box around the object
# #                     # Save the frame
# #                     # Send an API request...
# #
# #         writer.write(frame)
# #
# #
# #     # Show the video feed
# #     cv2.imshow('Frame', frame)
# #
# #     # Optional: Show the black & white difference mask to help you calibrate the MOTION_THRESHOLD
# #     # cv2.imshow('Motion Mask', thresh)
# #
# #     # 7. VERY IMPORTANT: Update the previous frame so we can compare it to the next one
# #     prev_gray = gray
# #
# #     if cv2.waitKey(20) & 0xFF == ord('q'):
# #         break
# #
# # cap.release()
# # writer.release()
# # cv2.destroyAllWindows()