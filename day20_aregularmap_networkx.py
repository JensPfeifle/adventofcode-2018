import matplotlib.pyplot as plt
from collections import defaultdict
import networkx as nx

example1 = "^WNE$"
example2 = "^ENWWW(NEEE|SSE(EE|N))$"
example3 = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
MYINPUT = open("data/day20").read().strip()


def get_distances(inp: str):
    global maze
    directions = iter(inp)

    distances = defaultdict(lambda: float('inf'))
    branches = {}
    branch = n = x = y = 0
    while True:
        c = next(directions)
        distances[(x, y)] = min(distances[(x, y)], n)  # store shortest path
        n = distances[(x, y)]  # length of shortest path to current loc
        if c == '$':
            break
        elif c == '(':
            branch += 1
            branches[branch] = (x, y, n)
        elif c == ')':
            branch -= 1
        elif c == '|':
            x, y, n = branches[branch]
        elif c == 'N':
            maze.add_edge((x, y), (x, y+1))
            y += 1
        elif c == 'S':
            y -= 1
            maze.add_edge((x, y), (x, y-1))
        elif c == 'E':
            x += 1
            maze.add_edge((x, y), (x+1, y))
        elif c == 'W':
            x -= 1
            maze.add_edge((x, y), (x-1, y))
        n += 1
    return distances


maze = nx.Graph()

distances = get_distances(MYINPUT)

ax = plt.subplot(111)
positions = {n: n for n in maze.nodes}
nx.draw_networkx(maze, pos=positions, with_labels=False,
                 node_size=5, style='dashed', ax=ax)
plt.show()
