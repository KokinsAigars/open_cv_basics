
# draw static rectangle on video stream
# drawing also text on top of video stream

import cv2
import datetime
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Error opening video stream or file')
    exit()

width =int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height =int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

x = width // 2
y = height // 2

# width && height of rectangle
w = width // 4
h = height // 4

# bottom right x + w, y+h

font = cv2.FONT_HERSHEY_SIMPLEX

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.rectangle(frame,(x,y),(x+w,y+h), color=(56, 150, 120), thickness=5)

    cv2.putText(frame, text='LIVE VIDEO', org=(10, 50), fontFace=font, fontScale=1, color=(255, 0, 255),
                thickness=3, lineType=cv2.LINE_AA)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (10, height - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
