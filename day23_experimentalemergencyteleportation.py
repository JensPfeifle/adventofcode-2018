from numba import njit
import re
from scipy.spatial import KDTree
import numpy as np
from typing import Dict, List

example = """\
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1"""

example2 = """\
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""

with open("data/day23", "r") as f:
    MYINPUT = f.read()

inp = MYINPUT
#inp = example2

numbr = re.compile(r"[\-0-9]+")

nanobots = {}
for n, nanobot in enumerate(inp.split('\n')):
    print(nanobot)
    x, y, z, r = (int(i) for i in re.findall(numbr, nanobot))
    nanobots[n] = (x, y, z, r)


def in_range(nanobots: Dict, queryidx: int) -> List[int]:
    """
    Get nanobots which are in range of nanobots[idx]
    In range means (Manhattan) distance <= r
    Returns list of indices which are in range
    """
    global kdtree
    querypt, radius = nanobots[queryidx][:-1], nanobots[queryidx][-1]
    # p=1->Manhattan distance
    return kdtree.query_ball_point(querypt, radius, p=1)


def overlap(nb1: (int), nb2: (int)) -> bool:
    """
    Check if the ranges of two nanobots overlap
    (Manhattan distance)
    """
    x1, y1, z1, r1 = nb1
    x2, y2, z2, r2 = nb2

    dx = abs(x2-x1)
    dy = abs(y2-y1)
    dz = abs(z2-z1)

    mindist = r1+r2
    dist = sum([dx, dy, dz])
    if dist > mindist:
        return False
    else:
        return True


def plotme():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 1)
    x, y, z = [], [], []
    for k, nb in nanobots.items():
        r = nb[3]
        points = [[nb[0], nb[1]+r], [nb[0]+r, nb[1]],
                  [nb[0], nb[1]-r], [nb[0]-r, nb[1]]]
        polygon = plt.Polygon(points, alpha=0.1)
        ax.add_patch(polygon)
        x.append(nb[0])
        y.append(nb[1])
        z.append(nb[2])

    ax.scatter(x, y)
    plt.show()


def setup(nanobots, distances):
    # could use sum of two biggest ranges instead of np.inf?
    overlaps = distances.copy()
    pairs = distances.keys()
    for nb1, nb2 in pairs:
        r = nanobots[nb1][3] + nanobots[nb2][3]
        if r > int(distances[(nb1, nb2)]):
            overlaps[(nb1, nb2)] = 1
        else:
            overlaps[(nb1, nb2)] = 0
    # add self
    for i in range(overlaps.shape[0]):
        overlaps[i, i] = 1
    print("Overlaps done")
    num_overlaps = np.sum(overlaps, axis=1)
    most_overlapping = set(nanobots[i]
                           for i in np.nonzero(overlaps[np.argmax(num_overlaps)])[1])
    return most_overlapping


@njit  # speeeed
def solve(overlapping_set, start=0):
    # increase distance from 0,0,0 until we are in range of all nanobots in the set
    distance_from_origin = start  # 112000000
    overlaps_all_of_set = False
    while not overlaps_all_of_set:
        overlaps_all_of_set = True
        fake_nb = (0, 0, 0, distance_from_origin)
        for nb in overlapping_set:
            x1, y1, z1, r1 = fake_nb
            x2, y2, z2, r2 = nb

            dx = abs(x2-x1)
            dy = abs(y2-y1)
            dz = abs(z2-z1)

            mindist = r1+r2
            dist = dx + dy + dz
            if dist > mindist:
                overlaps_all_of_set = False
        if distance_from_origin % 100000 == 0:
            print(distance_from_origin)
        distance_from_origin += 1
    return distance_from_origin


strongest_idx = max(nanobots, key=lambda n: nanobots[n][3])
strongest = nanobots[strongest_idx]
points = [nb[:-1] for k, nb in nanobots.items()]
kdtree = KDTree(points, leafsize=10)

print("Part 1")
print(in_range(nanobots, strongest_idx))
print(len(in_range(nanobots, strongest_idx)))

print("Part 2")
distances = kdtree.sparse_distance_matrix(kdtree, np.inf, p=1)
print("Distance matrix done")
most_overlapping = setup(nanobots, distances)
print("Solving...")
solve(most_overlapping)
