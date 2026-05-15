
# show video

import cv2
import time

cap = cv2.VideoCapture('output/myvideo001.mp4')

if not cap.isOpened():
    print('ERROR. File is not found, or wrong codec used!')
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # delay player at recorded speed for humans to watch
    # recorder at 20 FPS (frames/second)?
    time.sleep(1/20)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
