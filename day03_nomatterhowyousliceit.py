#!/usr/bin/python3

import time
import numpy as np
from typing import Tuple
#################
# Part 1
#################


def claim_to_slice(claim: str) -> Tuple:
    id_, _, xy, wh = claim.strip().split()
    x, y = xy.split(',')
    x = int(x)
    y = int(y[:-1])
    w, h = [int(s) for s in wh.split('x')]
    id_ = int(id_[1:])
    return id_, x, y, w, h


def overlapping_claims(claims: [str]) -> int:
    fabric = np.zeros((1000, 1000))

    for claim in claims:
        _, x, y, w, h = claim_to_slice(claim)
        fabric[x:x+w, y:y+h] += 1

    print("Max claims on one sq = " + str(fabric.max()))

    c = 0
    for row in fabric:
        for sqi in row:
            if sqi > 1:
                c += 1

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
    for claim in claims:
        i, x, y, w, h = claim_to_slice(claim)
        fabric[x:x+w, y:y+h] += 1

    for claim in claims:
        i, x, y, w, h  = claim_to_slice(claim)
        if np.all(fabric[x:x+w, y:y+h] == 1):
            intact.append(i)
    return intact


def part2test() -> None:
    claims = ['#1 @ 1,3: 4x4',
              '#2 @ 3,1: 4x4',
              '#3 @ 5,5: 2x2']
    print("testresult " + str(intact_claims(claims)))
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
