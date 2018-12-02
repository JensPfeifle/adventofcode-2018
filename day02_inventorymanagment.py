#!/usr/bin/python3

import time
from typing import Tuple
from collections import Counter


#################
# Part 1
#################

def idcheck(id: str) -> Tuple[bool, bool]:
    """
    Count the number of times any letter appears in the ID
    and return tuple of booleans if any letters show up
    exactly twice          (two_of_any,
    or exactly thrice       three_of_any)
    """
    counter = Counter(id)
    two_of_any = False
    three_of_any = False
    for letters, count in counter.items():
        if count == 2:
            two_of_any = True
        if count == 3:
            three_of_any = True
    return (two_of_any, three_of_any)


def checksum(IDs: [str]) -> int:
    a = 0
    b = 0
    for id_ in IDs:
        twos, threes = idcheck(id_)
        a += twos
        b += threes

    return a*b


def part1test():
    testinputs = ['abcdef',
                  'bababc',
                  'abbcde',
                  'abcccd',
                  'aabcdd',
                  'abcdee',
                  'ababab', ]

    assert idcheck('abcdef') == (False, False)
    assert idcheck('bababc') == (True, True)
    assert idcheck('abbcde') == (True, False)
    assert idcheck('abcccd') == (False, True)
    assert idcheck('aabcdd') == (True, False)
    assert idcheck('abcdee') == (True, False)
    assert idcheck('ababab') == (False, True)

    assert checksum(testinputs) == 12

    print("tests passed")


def part1(myinput: str) -> None:
    result = checksum(myinput)
    print("answer:" + str(result))


###############
# Part 2
###############

def get_duplicate_items(l: []):
	new = set()
	for item in l:
		if l.count(item) > 1:
			new.add( item )
	return list(new)


def find_similar_id(ids: [str]) -> str:
    """ 
    Return the characters which the two similar IDs have in common.
    Similar is defined as: identical except for a single different
    character in the same position in both IDs 
    """
    
    N = len(ids[0])
    for n in range(N):
        myids = [id_[:n] + id_[n+1:] for id_ in ids]
        for id_ in myids:
            if myids.count(id_) > 1:
                return id_


def part2test() -> None:
    testinputs = ['abcde',
                  'fghij',
                  'klmno',
                  'pqrst',
                  'fguij',
                  'axcye',
                  'wvxyz', ]
    assert find_similar_id(testinputs) == 'fgij'
    print("tests passed")


def part2(myinput: str) -> None:
    result = find_similar_id(myinput)
    print("answer:" + str(result.strip()))


###############
# Main
###############

if __name__ == "__main__":

    # my input
    with open('data/day2') as f:
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

