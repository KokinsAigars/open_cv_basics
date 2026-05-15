# src/video/video006.py
#
#   draw on live video
#
import cv2

## CALLBACK FUNCTION RECTANGLE
def draw_rectangle(event,x,y,flags,param):
    global pt1,pt2,topLeft_clicked,botRight_clicked

    if event == cv2.EVENT_LBUTTONDOWN:

        # RESET THE RECTANGLE
        if topLeft_clicked == True and botRight_clicked == True:
            pt1 = (0, 0)
            pt2 = (0, 0)
            topLeft_clicked = False
            botRight_clicked = False

        if topLeft_clicked == False:
            pt1 = (x, y)
            topLeft_clicked = True

        elif botRight_clicked == False:
            pt2 = (x, y)
            botRight_clicked = True

## GLOBAL VARIABLES
pt1 = (0,0)
pt2 = (0,0)
topLeft_clicked = False
botRight_clicked = False

## CONNECT TO CALLBACK
cap = cv2.VideoCapture(0)

cv2.namedWindow('Test')
cv2.setMouseCallback('Test',draw_rectangle)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    ## DRAWING ON THE FRAME BASED OFF THE GLOBAL VARIABLES
    if topLeft_clicked:
        cv2.circle(frame,center=pt1,radius=5,color=(120,120,50),thickness=-1)

    if topLeft_clicked and botRight_clicked:
        cv2.rectangle(frame,pt1,pt2,(70,34,200),3)

    cv2.imshow('Test', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

