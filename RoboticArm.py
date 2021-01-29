from tkinter import *
import serial
import numpy as np
import matplotlib.pyplot as plt
import math

ser = serial.Serial('COM9', 9600)
Servodegrees = [90, 90, 90, 90, 90, 90]


# 1:Base    2:Hand Rotation  3:Hand Tilt  4:Shoulder Tilt  5:Elbow Tilt  6:Hand Grab
def Printvalues():
    print()
    for x in range(len(Servodegrees)):
        if x == 1:
            print('Servo1 BASE: ' + str(Servodegrees[x]))
            print()
        elif x == 2:
            print('Servo2 Hand Rotation: ' + str(Servodegrees[x]))
            print()
        elif x == 3:
            print('Servo3 Hand Tilt: ' + str(Servodegrees[x]))

            print()
        elif x == 4:
            print('Servo4 Shoulder Tilt: ' + str(Servodegrees[x]))

            print()
        elif x == 5:
            print('Servo5 Elbow Tilt: ' + str(Servodegrees[x]))

            print()
        elif x == 6:
            print('Servo6 Hand Grab: ' + str(Servodegrees[x]))

            print()


def ScaleAdjust(value):
    if value == 'Base':
        var.set(Servodegrees[0])
    elif value == 'Hand Rotation':
        var.set(Servodegrees[1])
    elif value == 'Hand Tilt':
        var.set(Servodegrees[2])
    elif value == 'Shoulder Tilt':
        var.set(Servodegrees[3])
    elif value == 'Elbow Tilt':
        var.set(Servodegrees[4])
    elif value == 'Hand Grab':
        var.set(Servodegrees[5])


def translater(givenVal):
    if givenVal == 'Base':
        outputval = 'a'
    elif givenVal == 'Hand Rotation':
        outputval = 'b'
    elif givenVal == 'Hand Tilt':
        outputval = 'c'
    elif givenVal == 'Shoulder Tilt':
        outputval = 'e'
    elif givenVal == 'Elbow Tilt':
        outputval = 'd'
    elif givenVal == 'Hand Grab':
        outputval = 'f'
    return outputval


def Servo1Val(degrees):
    send = str(degrees)
    sendenc = send.encode()
    sendsvar = translater(variable.get())
    sendvar = sendsvar.encode()
    ser.write(sendvar)
    ser.write(sendenc)
    # print(sendenc)
    degrees = int(degrees)
    if sendsvar == 'a':
        Servodegrees[1] = degrees

    elif sendsvar == 'b':
        Servodegrees[2] = degrees

    elif sendsvar == 'c':
        Servodegrees[3] = degrees

    elif sendsvar == 'd':
        Servodegrees[4] = degrees

    elif sendsvar == 'e':
        Servodegrees[5] = degrees

    elif sendsvar == 'f':
        Servodegrees[6] = degrees
    update()


root = Tk()
var = DoubleVar()
scale = Scale(root, variable=var, orient=HORIZONTAL, from_=0, to=180, command=Servo1Val, length=300)
scale.pack(anchor=CENTER)

variable = StringVar(root)
variable.set("Base")  # default value
w = OptionMenu(root, variable, "Base", "Hand Rotation", "Hand Tilt", "Elbow Tilt", "Shoulder Tilt", "Hand Grab",
               command=ScaleAdjust)
w.pack()

button = Button(root, text="Print Values", command=Printvalues)
button.pack(anchor=CENTER)

label = Label(root)
label.pack()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plt.subplots_adjust(left=0.25, bottom=0.25)

First_Arm = 4
Second_ARM = 3.75
Third_arm = 2.5

zupdate = np.array([11.5, 11.5 + First_Arm * math.sin(Servodegrees[5]),
                    11.5 + First_Arm * math.sin(Servodegrees[5]) + (Second_ARM * math.sin(Servodegrees[3])),
                    11.5 + First_Arm * math.sin(Servodegrees[5]) + (
                            Second_ARM * math.sin(Servodegrees[3])) + Third_arm * math.sin(
                        Servodegrees[2])])
z = zupdate
xupdate = np.array([11.5, First_Arm * math.cos(Servodegrees[0]), First_Arm * math.cos(Servodegrees[0]),
                    First_Arm * math.cos(Servodegrees[0])])
x = xupdate
yupdate = np.array([11.5, First_Arm * math.cos(Servodegrees[5]),
                    First_Arm * math.cos(Servodegrees[5]) + (Second_ARM * np.cos(Servodegrees[3])),
                    First_Arm * math.cos(Servodegrees[5]) + (
                            Second_ARM * math.cos(Servodegrees[5])) + Third_arm * math.cos(
                        Servodegrees[2])])
y = yupdate
l, = plt.plot(x, y, z)


def update():
    zupdate = np.array([11.5, 11.5 + First_Arm * math.sin(Servodegrees[5]*np.pi/180),
                        11.5 + First_Arm * math.sin(Servodegrees[5]*np.pi/180) + (Second_ARM * math.sin((90-Servodegrees[5]+Servodegrees[4])*np.pi/180)),
                        11.5 + First_Arm * math.sin(Servodegrees[5]*np.pi/180) + (
                                Second_ARM * math.sin((90-Servodegrees[5]+Servodegrees[4])*np.pi/180)) + Third_arm * math.sin(
                            Servodegrees[3]*np.pi/180)])

    xupdate = np.array([0, First_Arm * math.cos(Servodegrees[1]*np.pi/180), First_Arm * math.cos(Servodegrees[1]*np.pi/180),
                        First_Arm * math.cos(Servodegrees[1]*np.pi/180)])

    yupdate = np.array([0, First_Arm * math.cos(Servodegrees[5]*np.pi/180),
                        First_Arm * math.cos(Servodegrees[5]*np.pi/180) + (Second_ARM * math.cos((90-Servodegrees[5]+Servodegrees[4])*np.pi/180)),
                        First_Arm * math.cos(Servodegrees[5]*np.pi/180) + (
                                Second_ARM * math.cos((90-Servodegrees[5]+Servodegrees[4])*np.pi/180)) + Third_arm * math.cos(
                            Servodegrees[3]*np.pi/180)])

    l.set_data(y, yupdate)
    l.set_data(x, xupdate)
    l.set_3d_properties(zupdate)
    print('X:', xupdate, '  Y:', yupdate, '  Z:', zupdate)
    print(Servodegrees)
    fig.canvas.draw_idle()


plt.show()

root.mainloop()
