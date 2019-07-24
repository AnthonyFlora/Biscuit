import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import collections
import random
import time
import datetime

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

xar1 = collections.deque(maxlen=10)
yar1 = collections.deque(maxlen=10)
yar2 = collections.deque(maxlen=10)
x = 0


def animate(i):
    global x
    x = datetime.datetime.fromtimestamp(time.time())
    y = random.randint(1, 5)
    xar1.append(x)
    yar1.append(int(y))
    yar2.append(int(y)+5)
    dates = matplotlib.dates.date2num(xar1)
    ax1.clear()
    ax1.plot(xar1, yar1, xar1, yar2)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()