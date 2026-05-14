
# drg mouse to create rectangle

import numpy as np
import matplotlib.pyplot as plt
import cv2

drawing = False
ix,iy = -1,-1

# Function
def draw_rectangle(event,x,y,flags,param):
    global drawing,ix,iy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(img,(ix,iy),(x,y),(10,73,160),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (10, 73, 160), -1)

# Create black image
img = np.zeros(shape=(512,512,3), dtype=np.int8)

cv2.namedWindow(winname='my_drawing')
cv2.setMouseCallback('my_drawing', draw_rectangle)

while True:

    cv2.imshow('my_drawing', img)

    # Esc key pressed?
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()

