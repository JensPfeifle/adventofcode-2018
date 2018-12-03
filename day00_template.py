#!/usr/bin/python3

import time


#################
# Part 1
#################

def part1test():
    print("tests passed")


def part1(myinput: str) -> None:
    result = None
    print("answer:" + str(result))


###############
# Part 2
###############

def part2test() -> None:
    print("tests passed")


def part2(myinput: str) -> None:
    result = None
    print("answer:" + str(result))


###############
# Main
###############

if __name__ == "__main__":

    # my input
    with open('data/day0') as f:
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
