

# Example to open images in separate window, but I skip that as I'm using Docker
# Will use Jupyter notebook to display images not adding complexity to docker

import cv2

img = cv2.imread('/home/ak/IdeaProjects/open_cv_basics/output/00-puppy.jpg')
if img is None:
    raise FileNotFoundError("Image not found!")

while True:
    # Use native cv2.imshow (no RGB conversion needed!)
    cv2.imshow('Puppy Window', img)

    # waitKey now has a window to listen to
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()




# IF we've waited at least 1 ms AND we've pressed the Esc key
# if cv2.waitKey(1) & 0xFF == 27:
#     break

# if cv2.waitKey(1) & 0xFF == ord('q'):  # Use ord('q') to get the integer value
#     break