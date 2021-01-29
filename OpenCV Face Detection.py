import cv2
import time
import serial

ser = serial.Serial('COM9', 9600)
Servodegrees = [60, 90, 30, 0, 30, 0]
ServoName = ['a', 'b', 'c', 'd', 'f']
stepsx = 1
stepsmax = 30
stepsy = 1
stepsmay = 30
xDIFF = 30
yDIFF = 30
setup = True


def acceleration_displacement(distancex, distancey):
    stepsx = 1 + int(stepsmax * distancex / cap.get(3)) ** 2
    stepsy = 1 + int(stepsmay * distancey / cap.get(4)) ** 2


# 1:Base    2:Hand Rotation  3:Hand Tilt  4:Elbow Tilt  5:Shoulder Tilt  6:Hand Grab


def servofollower(morelessX, morelessY):
    if morelessX == 'more':
        if Servodegrees[0] <= (180 - stepsx):
            Servodegrees[0] = Servodegrees[0] + stepsx
            Servo1Val(Servodegrees[0], 'a')
    elif morelessX == 'less':
        if Servodegrees[0] >= (0 + stepsx):
            Servodegrees[0] = Servodegrees[0] - stepsx
            Servo1Val(Servodegrees[0], 'a')
    else:
        pass
    if morelessY == 'less':
        if Servodegrees[2] <= (180 - stepsx):
            Servodegrees[2] = Servodegrees[2] + stepsy
            Servo1Val(Servodegrees[2], 'c')
    elif morelessY == 'more':
        if Servodegrees[2] >= (0 + stepsy):
            Servodegrees[2] = Servodegrees[2] - stepsy
            Servo1Val(Servodegrees[2], 'c')
    else:
        pass


def Servo1Val(degrees, servo):
    send = str(degrees)
    sendenc = send.encode()
    sendsvar = servo
    sendvar = sendsvar.encode()
    ser.write(sendvar)
    ser.write(sendenc)
    print(sendenc)
    if sendsvar == 'a':
        Servodegrees[0] = degrees

    elif sendsvar == 'b':
        Servodegrees[1] = degrees

    elif sendsvar == 'c':
        Servodegrees[2] = degrees

    elif sendsvar == 'd':
        Servodegrees[3] = degrees

    elif sendsvar == 'e':
        Servodegrees[4] = degrees

    elif sendsvar == 'f':
        Servodegrees[5] = degrees


# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)
# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')

while True:
    # Read the frame
    _, img = cap.read()
    width = cap.get(3)  # float
    height = cap.get(4)  # float
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # Display
    cv2.imshow('img', img)
    for (x, y, w, h) in faces:
        while setup:
            for i in range(5):
                Servo1Val(Servodegrees[i], ServoName[i])
            time.sleep(1)
            setup = False

        if (x + w / 2) < (width / 2) and ((width / 2) - (x + w / 2)) > xDIFF:
            distance = (width / 2) - (x + w / 2)
            acceleration_displacement(distance, 0)
            servofollower('more', '')
        elif (x + w / 2) > (width / 2) and ((x + w / 2) - (width / 2)) > xDIFF:
            distance = (x + w / 2) - (width / 2)
            acceleration_displacement(distance, 0)
            servofollower('less', '')
        if (y + h / 2) > (height / 2) and ((y + h / 2) - (height / 2)) > yDIFF:
            distance = (y + h / 2) - (height / 2)
            acceleration_displacement(0, distance)
            servofollower('', 'more')
        elif (y + h / 2) < (height / 2) and ((height / 2) - (y + h / 2)) > yDIFF:
            distance = (height / 2) - (y + h / 2)
            acceleration_displacement(0, distance)
            servofollower('', 'less')

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
# Release the VideoCapture object
cap.release()
