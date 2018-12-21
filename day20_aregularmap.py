from collections import defaultdict

example1 = "^WNE$"
example2 = "^ENWWW(NEEE|SSE(EE|N))$"
example3 = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
MYINPUT = open("data/day20").read().strip()


def get_distances(inp: str):
    directions = iter(inp)

    distances  = defaultdict(lambda : float('inf'))
    branches = {}
    branch = n = x = y = 0
    while True:
        c = next(directions)
        distances[(x,y)] = min(distances[(x,y)], n) # store shortest path
        n = distances[(x,y)] # length of shortest path to current loc
        if c == '$':
            break
        elif c == '(':
            branch += 1
            branches[branch] = (x,y,n)
        elif c == ')':
            branch -= 1
        elif c == '|':
            x,y,n = branches[branch]
        elif c == 'N':
            y += 1
        elif c == 'S':
            y -= 1
        elif c == 'E':
            x += 1
        elif c == 'W':
            x -= 1
        n += 1
    return distances

#tests
d = get_distances(example1)
assert max(d.items(), key = lambda x: x[1])[1] == 3
d = get_distances(example2)
assert max(d.items(), key = lambda x: x[1])[1] == 10
d = get_distances(example3)
assert max(d.items(), key = lambda x: x[1])[1] == 18

distances = get_distances(MYINPUT)
print("Part 1")
print(max(distances.items(), key = lambda x: x[1]))

print("Part 2")
print(len([k for k,v in distances.items() if v >= 1000]))

