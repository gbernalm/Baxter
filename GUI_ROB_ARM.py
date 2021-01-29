import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plt.subplots_adjust(left=0.25, bottom=0.25)

Servodegrees = [60, 90, 30, 0, 30, 0]

First_Arm = 4
Second_ARM = 3.75
Third_arm = 2.5

zupdate = np.array([11.5, 11.5 + First_Arm * np.sin(Servodegrees[4]),
                    11.5 + First_Arm * np.sin(Servodegrees[4]) + (Second_ARM * np.sin(Servodegrees[3])),
                    11.5 + First_Arm * np.sin(Servodegrees[4]) + (
                            Second_ARM * np.sin(Servodegrees[3])) + Third_arm * np.sin(
                        Servodegrees[2])])
z = zupdate
xupdate = np.array([11.5, First_Arm * np.cos(Servodegrees[0]), First_Arm * np.cos(Servodegrees[0]),
                    First_Arm * np.cos(Servodegrees[0])])
x = xupdate
yupdate = np.array([11.5, First_Arm * np.cos(Servodegrees[4]),
                    First_Arm * np.cos(Servodegrees[4]) + (Second_ARM * np.cos(Servodegrees[3])),
                    First_Arm * np.cos(Servodegrees[4]) + (
                            Second_ARM * np.cos(Servodegrees[3])) + Third_arm * np.cos(
                        Servodegrees[2])])
y = yupdate
l, = plt.plot(x, y, z)


def update():
    l.set_data(y, yupdate)
    l.set_data(x, yupdate)
    l.set_3d_properties(zupdate)
    fig.canvas.draw_idle()
plt.show()