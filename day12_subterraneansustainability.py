#!/usr/bin/python3
from copy import copy


def evaluate(LLCRR):
    if LLCRR == ".#.##": return "."
    if LLCRR == ".####": return "."
    if LLCRR == "#..#.": return "."
    if LLCRR == "##.##": return "#"
    if LLCRR == "..##.": return "#"
    if LLCRR == "##...": return "#"
    if LLCRR == "..#..": return "#"
    if LLCRR == "#.##.": return "."
    if LLCRR == "##.#.": return "."
    if LLCRR == ".###.": return "#"
    if LLCRR == ".#.#.": return "#"
    if LLCRR == "#..##": return "#"
    if LLCRR == ".##.#": return "#"
    if LLCRR == "#.###": return "#"
    if LLCRR == ".##..": return "#"
    if LLCRR == "###.#": return "."
    if LLCRR == "#.#.#": return "#"
    if LLCRR == "#....": return "."
    if LLCRR == "#...#": return "."
    if LLCRR == ".#...": return "#"
    if LLCRR == "##..#": return "."
    if LLCRR == "....#": return "."
    if LLCRR == ".....": return "."
    if LLCRR == ".#..#": return "#"
    if LLCRR == "#####": return "."
    if LLCRR == "#.#..": return "."
    if LLCRR == "..#.#": return "#"
    if LLCRR == "...##": return "."
    if LLCRR == "...#.": return "#"
    if LLCRR == "..###": return "."
    if LLCRR == "####.": return "#"
    if LLCRR == "###..": return "#"
    return False


def evaluate_example(LLCRR):
    if LLCRR == "...##": return "#"
    if LLCRR == "..#..": return "#"
    if LLCRR == ".#...": return "#"
    if LLCRR == ".#.#.": return "#"
    if LLCRR == ".#.##": return "#"
    if LLCRR == ".##..": return "#"
    if LLCRR == ".####": return "#"
    if LLCRR == "#.#.#": return "#"
    if LLCRR == "#.###": return "#"
    if LLCRR == "##.#.": return "#"
    if LLCRR == "##.##": return "#"
    if LLCRR == "###..": return "#"
    if LLCRR == "###.#": return "#"
    if LLCRR == "####.": return "#"
    return "."

def score(pts, zp):
    score = 0
    for i in range(len(pts)):
        value = i - zp
        #print(value)
        #print(pots[i])
        if pts[i] == "#": 
            score += value
    return score

initial_state = "#......##...#.#.###.#.##..##.#.....##....#.#.##.##.#..#.##........####.###.###.##..#....#...###.##"
#initial_state = "#..#.#..##......###...###"
pots = "..." + initial_state + "...."


zero_pot = 3
print("{}: {}\t{}".format(0, pots, zero_pot))
steady_gens = 200
for n in range(steady_gens):
    nextgen = ".."
    for i in range(2, len(pots) - 2):
        nextgen += evaluate(pots[i-2:i+3])
    if nextgen.endswith("#"):
        nextgen += "..."   
    if nextgen.startswith("..#"):
        nextgen = "..." + nextgen          
        zero_pot += 3
    pots  = nextgen + ".."
    print("{}: {}\t{}".format(n+1, pots, zero_pot))
    print("score: " + str(score(pots, zero_pot)))

print("Steady state reached")
scr = score(pots, zero_pot) + 75 * (50000000000 - steady_gens)
print("extrapolated " + str(scr))


