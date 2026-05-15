import numpy as np
import matplotlib.pyplot as plt
import cv2

# Function
def draw_circle(event,x,y,flags,param):

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img,(x,y),15,(0,255,0),-1)

    elif even == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(img,(x,y),10,(250,40,10),-1)

cv2.namedWindow(winname='my_drawing')

cv2.setMouseCallback('my_drawing', draw_circle)


# showing image
img = np.zeros(shape=(512,512,3), dtype=np.int8)

while True:

    cv2.imshow('my_drawing', img)

    if cv2.waitKey(20) & 0xFF == ord('q'):  # Use ord('q') to get the integer value
        break

cv2.destroyAllWindows()

