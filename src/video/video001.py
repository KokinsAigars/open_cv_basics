
# capture video from camera

import cv2

cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
    print('Error opening video stream or file')
else:
    fps = cap.get(5)
    print('Frames per second : ', fps, 'FPS')

    frame_count = cap.get(7)
    print('Frame count : ', frame_count)


width =int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height =int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# WINDOWS -- *'DIVX'
# LINUX -- *'XVID'
writer = cv2.VideoWriter('output/myvideo001.mp4',cv2.VideoWriter_fourcc(*'DIVX'),20,(width,height))

while(cap.isOpened()):

    ret, frame = cap.read()
    if ret == True:
        cv2.imshow('Frame', frame)
        writer.write(frame)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    else:
        break


cap.release()
writer.release()
cv2.destroyAllWindows()
