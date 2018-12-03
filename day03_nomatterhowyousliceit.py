#!/usr/bin/python3

import time
import numpy as np
from typing import Tuple
#################
# Part 1
#################



def parse_claims(claims: [str]) -> [Tuple]:
    """
    Parse claims from string to list of tuples of claim properties.
    """
    parsed_claims = []
    for claim in claims:
        id_, _, xy, wh = claim.strip().split()
        x, y = xy.split(',')
        x = int(x)
        y = int(y[:-1])
        w, h = [int(s) for s in wh.split('x')]
        id_ = int(id_[1:])
        parsed_claims.append((id_, x, y, w, h))
    return parsed_claims

def overlapping_claims(claims: [str]) -> int:
    fabric = np.zeros((1000, 1000))

    for claim in parse_claims(claims):
        _, x, y, w, h = claim
        fabric[x:x+w, y:y+h] += 1

    #c = 0
    #for row in fabric:
    #    for sqi in row:
    #        if sqi > 1:
    #            c += 1
    c = np.sum(fabric > 1)
    

    return c


def part1test():
    claims = ['#1 @ 1,3: 4x4',
              '#2 @ 3,1: 4x4',
              '#3 @ 5,5: 2x2']
    assert overlapping_claims(claims) == 4
    print("tests passed")


def part1(myinput: str) -> None:
    result = overlapping_claims(myinput)
    print("answer:" + str(result))


###############
# Part 2
###############

def intact_claims(claims: [str]) -> [int]:
    intact = []
    fabric = np.zeros((1000, 1000))
    for claim in parse_claims(claims):
        i, x, y, w, h = claim
        fabric[x:x+w, y:y+h] += 1

    for claim in parse_claims(claims):
        i, x, y, w, h  = claim
        if np.all(fabric[x:x+w, y:y+h] == 1):
            intact.append(i)
    return intact


def part2test() -> None:
    claims = ['#1 @ 1,3: 4x4',
              '#2 @ 3,1: 4x4',
              '#3 @ 5,5: 2x2']
    assert intact_claims(claims) == [3]
    print("tests passed")


def part2(myinput: str) -> None:
    result = intact_claims(myinput)
    print("answer:" + str(result))


###############
# Main
###############

if __name__ == "__main__":

    # my input
    with open('data/day3') as f:
        MYINPUT = f.readlines()

    print("Part 1:")
    part1test()
    t0 = time.time()
    part1(MYINPUT)
    print("time: " + str(time.time() - t0))

    print("Part 2:")
    part2test()
    t0 = time.time()
    part2(MYINPUT)
    print("time: " + str(time.time() - t0))
