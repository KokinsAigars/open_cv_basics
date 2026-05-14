import numpy as np
import matplotlib.pyplot as plt
import cv2

img = cv2.imread('../output/scatter_plot.png')
# Convert BGR to RGB for correct colors
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
