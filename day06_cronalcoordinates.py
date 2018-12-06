#!/usr/bin/python3
import time
import sys

from collections import defaultdict

with open('data/day6', 'r') as f:
    myinput = f.read().strip().split('\n')


X = [int(coords.strip().split(',')[0]) for coords in myinput]
Y = [int(coords.strip().split(',')[1]) for coords in myinput]
XY = list(zip(X,Y))

names = [chr(i).upper() for i in range(97, 97+26)]
names += [chr(i).upper()+chr(i).upper() for i in range(97, 97+26)]

assert len(XY) <= len(names), "too many locations for names"

manhattan = lambda p,q: (abs(p[0]-q[0])+abs(p[1]-q[1]))

min_x = min(X)-1000
max_x = max(X) + 1000
min_y = min(Y) - 1000
max_y = max(Y) + 1000

grid = {}
areas = defaultdict(int)

for i in range(min_x, max_x+1):
    for j in range(min_y, max_y+1):
        closest = XY[0]
        closest_dist = sys.maxsize
        for xy in XY:
            dist = manhattan(xy, (i,j))
            if dist < closest_dist:
                closest_dist = dist
                closest = xy
            elif dist == closest_dist and closest != xy:
                closest = None
            grid[(i,j)] = closest
        areas[closest] += 1

print(sorted(areas.items(), key=lambda x: x[1]))


if __name__ == "__main__":
    pass
    #print(myinput)
#
    #print("Part 1:")
    #t0 = time.time()
    #print("time: " + str(time.time() - t0))
#
    #print("Part 2:")
    #t0 = time.time()
    #print("time: " + str(time.time() - t0))
