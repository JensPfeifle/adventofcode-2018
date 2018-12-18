import numpy as np
import copy

testinput= \
"""
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""

def to_str(field):
    fieldstring = ""
    for x in range(field.shape[0]):
        for y in range(field.shape[1]):
            fieldstring += "".join(inv_map[collectionarea[x,y]])
        fieldstring = fieldstring + "\n"
    return fieldstring

def to_ndarray(fieldstring):
    arr = []
    rows = fieldstring.strip().split("\n")
    for n in range(len(rows)):
        arr.append([map_[s] for s in rows[n]])
    
    return np.array(arr)


def resource_value(field):
    wooded_acres = collectionarea.flatten().tolist().count(TREE) 
    nlbyards = collectionarea.flatten().tolist().count(LBYARD)  

    return wooded_acres * nlbyards

collectionarea = np.zeros([50,50], dtype=int)

OPEN = 0
TREE = 1
LBYARD = 3

map_ = {'.':OPEN,'|':TREE, '#':LBYARD}
inv_map = {v: k for k, v in map_.items()}

with open('data/day18', 'r') as f:
    myinput = f.read()

for i,row in enumerate(myinput.strip().splitlines()):
    for j,contents in enumerate(row):
        collectionarea[i][j] = map_[contents]


def loop(maxtime):

    global collectionarea
    snapshots = []
    firstrepeat = None
    t = 0
    while t < maxtime:

        #print("============================")
        #print(t)
        #print(to_str(collectionarea))

        future_collectionarea = copy.deepcopy(collectionarea)
        for x in range(collectionarea.shape[0]):
            for y in range(collectionarea.shape[1]):
                ntrees = 0
                nlbyards = 0
                for i in range(x-1,x+2):
                    if i >= 0 and i < collectionarea.shape[0]:
                        for j in range(y-1, y+2):
                            if j >= 0 and j < collectionarea.shape[0] and not (i,j) == (x,y):
                                if collectionarea[i,j] == TREE:
                                    ntrees += 1
                                elif collectionarea[i,j] == LBYARD:
                                    nlbyards += 1
        #        print("[{},{}]: {} trees {} lbyards".format(x,y,ntrees, nlbyards))
                if collectionarea[x,y] == OPEN:
                    if ntrees >= 3:
        #                print("[{},{}] becomes {}".format(x,y,'TREE'))
                        future_collectionarea[x,y] = TREE
                elif collectionarea[x,y] == TREE:
                    if nlbyards >= 3:
        #                print("[{},{}] becomes {}".format(x,y,'LBYARD'))
                        future_collectionarea[x,y] = LBYARD
                elif collectionarea[x,y] == LBYARD:
                    if ntrees > 0 and nlbyards > 0:
                        pass
        #                print("[{},{}] remains {}".format(x,y,'LBYARD'))
                    else:
        #                print("[{},{}] becomes {}".format(x,y,'OPEN'))
                        future_collectionarea[x,y] = OPEN
        collectionarea = future_collectionarea
        # detect looping 
        if to_str(collectionarea) in snapshots:
            if not firstrepeat:
                firstrepeat = (to_str(collectionarea), t)
            else:
                if to_str(collectionarea) == firstrepeat[0]:
                    print(str(firstrepeat[1]) + "<-" + str(t))
                    print("period is " + str(t - firstrepeat[1]))
                    looptime = maxtime % (t - firstrepeat[1])
                    print("looptime " + str(looptime))
                    return to_ndarray(snapshots[firstrepeat[1] + looptime])
        snapshots.append(to_str(collectionarea))
        del future_collectionarea
        t+= 1
    return collectionarea


print("part1")
print(resource_value(loop(maxtime = 10)))
print("part2")
print(resource_value(loop(maxtime = 1000000000)))

    
    #An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
    #An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
    #An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.



    
