#!/usr/bin/python3
import time

lc = [chr(i) for i in range(97, 97+26)]
uc = [c.upper() for c in lc]
reactants = [r[0] + r[1] for r in zip(lc, uc)]
reversedreactants = [r[::-1] for r in reactants]


def react_all(polymer: str) -> str:
    while True:
        len_before = len(polymer)
        for r in reactants:
            polymer = polymer.replace(r, '')
        for rr in reversedreactants:
            polymer = polymer.replace(rr, '')

        if len(polymer) == len_before:
            return polymer


def remove_and_react(polymer: str, unittype: str) -> str:
    u = unittype
    u2 = unittype.upper()

    polymer = polymer.replace(u, '')
    polymer = polymer.replace(u2, '')
    return react_all(polymer)


def tests():
    assert react_all('aA') == ''

    assert react_all('abBA') == ''
    assert react_all('abAB') == 'abAB'
    assert react_all('aabAAB') == 'aabAAB'

    example_result = react_all('dabAcCaCBAcCcaDA')
    assert len(example_result) == 10

    assert len(remove_and_react('dabAcCaCBAcCcaDA', 'a')) == 6
    assert len(remove_and_react('dabAcCaCBAcCcaDA', 'b')) == 8
    assert len(remove_and_react('dabAcCaCBAcCcaDA', 'c')) == 4
    assert len(remove_and_react('dabAcCaCBAcCcaDA', 'd')) == 6

    assert part2('dabAcCaCBAcCcaDA') == 4


def part2(polymer: str) -> int:
    lc = [chr(i) for i in range(97, 97+26)]
    lens = [(u, len(remove_and_react(polymer, u))) for u in lc]
    lens.sort(key=lambda x: x[1])
    return(lens[0][1])

if __name__ == "__main__":

    with open('data/day5', 'r') as f:
        myinput = f.read().strip()

    print("Part 1:")
    t0 = time.time()
    result = react_all(myinput)
    print(len(result))
    print("time: " + str(time.time() - t0))

    print("Part 2:")
    t0 = time.time()
    print(part2(myinput))
    print("time: " + str(time.time() - t0))
