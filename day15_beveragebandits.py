from typing import Tuple
from collections import namedtuple
import numpy as np


class Unit():


    def __init__(self, initialpos, alive = True):
        self.pos = initialpos
        self.alive = alive

    def in_range(self):
        x = self.pos[0]
        y = self.pos[1]
        return [(x,y-1),
                (x+1,y),
                (x,y+1),
                (x-1,y)]

    def __repr__(self):
        return "{} {}".format('U', self.pos)

class Elf(Unit):
    def __repr__(self):
        return "{} {}".format('E', self.pos)

class Goblin(Unit):
    def __repr__(self):
        return "{} {}".format('G', self.pos)


def printf():
    global field
    global units

    for y, row in enumerate(field):
        for x, square in enumerate(row):
            empty = True
            for u in units:
                if u.pos == (x,y):
                    empty = False
                    if type(u) == Elf:
                        print('E', end="")
                    else:
                        print('G', end="")
            if empty:
                print(square, end="")
        print("")

testinput = \
"""\
#######
#.....#
#.....#
#..EG.#
#######\
"""

units = []
field = testinput.split("\n")
field_shape = (len(field), len(field[0]))
for y, row in enumerate(field):
    for x, square in enumerate(row):
        print(x,y, square)
        if square == 'E':
            units.append(Elf((x,y), alive=True))
        elif square == 'G':
            units.append(Goblin((x,y), alive=True))
field = [f.replace('E','.').replace('G','.') for f in field]

units.sort(key=lambda u: (u.pos[1],u.pos[0]))
for unit in units:
    targets = [u for u in units if u != unit]
    print(unit)
    print(unit.in_range())
    for t in targets:
        in_range_and_open = [p for p in t.in_range() if field[p[1]][p[0]] == '.']
        print(in_range_and_open)
        for p in in_range_and_open:
            if any(unit.in_range()) == p:
                print(" {}: {} in range!".format(unit, p))


printf()