#!/usr/bin/python3

import networkx as nx

rocky, wet, narrow = 0, 1, 2
torch, gear, neither = 0, 1, 2
valid_tools = {rocky: (torch, gear),
               wet: (gear, neither),
               narrow: (torch, neither)}
valid_regions = {torch: (rocky, narrow),
                 gear: (rocky, wet),
                 neither: (wet, narrow)}


def generate_map(depth: int, max_x: int, max_y: int) -> {}:
    # def generate_map(depth, max_x, max_y):
    """
    Takes cave depth & target
    Returns map of cave as dict of ({x,y):type}
    """

    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x, y) == (0, 0):
                geoindex[(0, 0)] = 0
            elif (x, y) == target:
                geoindex[target] = 0
            elif y == 0:
                geoindex[(x, y)] = x*16807
            elif x == 0:
                geoindex[(x, y)] = y*48271
            else:
                geoindex[(x, y)] = erolevel[(x-1, y)] * erolevel[(x, y-1)]
            erolevel[(x, y)] = (geoindex[(x, y)] + depth) % 20183
            types[(x, y)] = erolevel[(x, y)] % 3
    return types


def print_map(cave, max_x, max_y):
    # print cave map
    for y in range(max_y):
        x_values = [{0: ".", 1: "=", 2: "|"}[
            types[(x, y)]] for x in range(max_x)]
        if y == target[1]:
            x_values[target[0]] = "T"
        print("".join(x_values))


def print_map_path(cave, path, max_x, max_y):
    # print cave map with path
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) == target:
                print("X", end="")
            elif (x, y) in [(p[0], p[1]) for p in path]:
                print("*", end="")
            else:
                print({0: ".", 1: "=", 2: "|"}[types[(x, y)]], end="")
        print("")


def shortest_path(types, target, max_x, max_y):
    maze = nx.Graph()
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) == (0, 0):
                maze.add_node((0, 0, torch))
            cur_type = types[(x, y)]
            cur_tools = valid_tools[cur_type]
            # switch tool and don't move
            maze.add_edge((x, y, cur_tools[0]),
                          (x, y, cur_tools[1]), weight=7)
            # print("toolswitch" + str((x, y, cur_tools[0])) +
            #      str((x, y, cur_tools[1])))
            # or move
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x <= max_x and 0 <= new_y <= max_y:
                    valid_in_new = valid_tools[types[(new_x, new_y)]]
                    for t in set(cur_tools) & set(valid_in_new):
                        # print("added" + str((x, y, t)) +
                        #      str((new_x, new_y, t)))
                        maze.add_edge((x, y, t), (new_x, new_y, t), weight=1)
    path = nx.dijkstra_path(maze, source=(0, 0, torch),
                            target=(target[0], target[1], torch))
    path_length = nx.dijkstra_path_length(maze, source=(0, 0, torch),
                                          target=(target[0], target[1], torch))
    return path, path_length


# MYINPUT
depth = 11394
target = (7, 701)

# EXAMPLE
depth = 510
target = (10, 10)

max_x = (target[0]+1) * 8
max_y = (target[1]+1) * 2

geoindex = {}
erolevel = {}
types = {}

print("Part1")
types = generate_map(depth, max_x, max_y)
risklevel = sum([t for pos, t in types.items() if not pos == target])
print(risklevel)

print("Part2")
#  one possibility:
#  A*-Algorithm
#  https://de.wikipedia.org/wiki/A*-Algorithmus
# another: networkx
p, pl = shortest_path(types, target, max_x, max_y)
print_map_path(types, p, max_x, max_y)
print(pl)
