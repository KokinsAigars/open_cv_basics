# src/image_processing/ip001.py
#
# Color convert
#

import cv2
import matplotlib.pyplot as plt

img = cv2.imread('output/00-puppy.jpg')
if img is None:
    raise FileNotFoundError("Image not found!")

img_rgb = img
# img_rgb = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# img_rgb = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
# img_rgb = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)

while True:

    cv2.imshow('Puppy', img_rgb)

    if cv2.waitKey(20) & 0xFF == ord('q'):  # Use ord('q') to get the integer value
        break

cv2.destroyAllWindows()
