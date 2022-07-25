import os
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
# variables
width = 1280
height = 720

# video capture
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# getting images for presentation
folderPath = "presentation"
pathImages = sorted(os.listdir(folderPath), key=len)

# variables
imgNumber = 0
hs, ws = int(120), int(213)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 10
annotations = [[]]
annotationNumber = 0
annotationStart = False

# hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# getting image from camera
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)
    imgCurrent = cv2.resize(imgCurrent, (1280, 720))

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold),
             (width, gestureThreshold), (0, 255, 0), 10)
    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        # print(fingers)
        cx, cy = hand['center']
        lmList = hand['lmList']

        # constraints to draw a pointer
        indexFingure = lmList[8][0], lmList[8][1]
        xVal = int(np.interp(lmList[8][0], [width/2, w], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFingure = xVal, yVal

        # if hand is at the height of face
        if cy <= gestureThreshold:
            annotationStart = False
            # gesture 1
            if fingers == [1, 0, 0, 0, 0]:
                print("GO left ")
                annotationStart = False

                if imgNumber > 0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0

                    imgNumber -= 1
            # gesture 2
            if fingers == [0, 0, 0, 0, 1]:
                print("GO right ")
                annotationStart = False

                if imgNumber < len(pathImages)-1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0

                    imgNumber += 1

        # gesture 3 show pointer
        if fingers == [0, 1, 1, 0, 0]:
            annotationStart = False
            cv2.circle(imgCurrent, indexFingure, 12, (0, 0, 255), cv2.FILLED)

        # gesture 4 draw pointer
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurrent, indexFingure, 12, (0, 0, 255), cv2.FILLED)
            annotations[annotationNumber].append(indexFingure)
        else:
            annotationStart = False

        # gesture 5 erase
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                if annotationNumber >= 0:
                    annotations.pop(-1)
                    annotationNumber -= 1
                    buttonPressed = True

    else:
        annotationStart = False
    # button pressed iterations
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter >= buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(
                    imgCurrent, annotations[i][j-1], annotations[i][j], (0, 0, 200), 12)

    # adding webcam image on slide
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w-ws:w] = imgSmall

    # show images
    cv2.imshow("Imaage", img)
    cv2.imshow("Slides", imgCurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
