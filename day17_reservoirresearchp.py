import re
import numpy as np
import matplotlib.pyplot as plt

testinput = """\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504\
"""

def plotme():
    global grid

    plt.spy(grid.T)
    plt.show()
    # plt.gca().invert_yaxis()

# air            . : 0
# flowing water  | : 1
# standing water ~ : 2
# clay           # : 3

AIR = 0
WATERF = 1
WATERS = 2
CLAY = 3

rex = re.compile(r"x=[0-9.]*")
rey = re.compile(r"y=[0-9.]*")

spring_location = (500, 0)  # at top of area

clay_x = []
clay_y = []
for line in testinput.splitlines():
    print(line)
    xinput = re.findall(rex, line)[0]
    yinput = re.findall(rey, line)[0]
    # .. either in x or y, never both or neither
    if ".." in xinput:
        xinput = xinput.split("..")
        x = list(range(int(xinput[0][2:]), int(xinput[1])+1))
        y = [int(yinput[2:])] * len(x)
    else:
        yinput = yinput.split("..")
        y = list(range(int(yinput[0][2:]), int(yinput[1])+1))
        x = [int(xinput[2:])] * len(y)
    clay_x.extend(x)
    clay_y.extend(y)

min_x = min(clay_x)
max_x = max(clay_x)
min_y = min(clay_y)
max_y = max(clay_y)

grid = np.zeros([max_x-min_x+3, max_y + 1],dtype=int)

assert len(clay_x) == len(clay_y)
for n in range(len(clay_x)):
    grid[clay_x[n]-min_x+1, clay_y[n]] = 3
print(clay_x)
print(grid)

grid[spring_location[0]-min_x+1, spring_location[1]] = 1

while True:
    old_grid = grid.copy()

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x,y] == WATERF:
                if y+1 < grid.shape[1]:
                    grid[x,y+1] = WATERF
            if grid[x,y+1] == CLAY:
                grid[x,y] = WATERS

    print("---")
    print(grid.T)
    if np.all(old_grid == grid):
        break
    
