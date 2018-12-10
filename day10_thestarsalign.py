
import matplotlib.pyplot as plt
import numpy as np
import re
from collections import Counter

numbers = re.compile(r"([\-0-9]+)")

exampledata = """
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""

with open("data/day10", "r") as f:
    data = f.read().strip().split("\n")

#data = exampledata.strip().split("\n")

x0 = np.zeros(len(data),dtype=int)
y0 = np.zeros(len(data),dtype=int)
dx = np.zeros(len(data),dtype=int)
dy = np.zeros(len(data),dtype=int)

for n, dataline in enumerate(data):
    x_,y_,dx_,dy_ = ([int(i) for i in re.findall(numbers, dataline)])
    x0[n] = x_
    y0[n] = y_
    dx[n] = dx_
    dy[n] = dy_

maxcount = 0
tmessage = 0
for t in range(15000):
    x = x0 + t*dx
    y = y0 + t*dy
    cx = sum([t[1] for t in Counter(x).most_common()[:3]])
    cy = sum([t[1] for t in Counter(y).most_common()[:3]])
    if cx + cy > maxcount:
        print(t, cx+cy)
        maxcount = cx+cy
        tmessage = t

x = x0 + tmessage*dx
y = y0 + tmessage*dy
y = -y # flipit!
plt.ylim(-140, -80)
plt.scatter(x,y, s = 1)
plt.show()