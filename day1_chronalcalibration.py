#!/usr/bin/python3

#################
# Part 1
#################


def calc_frequency(sequence: [], f=0) -> int:
    """
    sequence: sequence of frequency changes
    f: initial frequency f
    """
    for df in sequence:
        f = f + df
    return f


def input_to_sequence(inputstr: str) -> []:
    seq = [int(l) for l in inputstr.split()]
    return seq


def part1test():
    # test examples
    testinput = """
    +1
    -2
    +3
    +1
    """
    testinput_sequence = [1, -2, 3, 1]

    assert (input_to_sequence(testinput) == testinput_sequence)

    assert (calc_frequency([1, -2, 3, 1]) == 3)
    assert (calc_frequency([1, 1, 1]) == 3)
    assert (calc_frequency([1, 1, -2]) == 0)
    assert (calc_frequency([-1, -2, -3]) == -6)
    print("tests passed")


def part1(myinput: str) -> None:
    result = calc_frequency(input_to_sequence(myinput))
    print("answer:" + str(result))


###############
# Part 2
###############


def find_repeatedfreq(sequence: [], f=0) -> int:
    freqs = [f]
    i = 0  # sequence index
    while True:
        f = freqs[-1] + sequence[i]
        if f not in freqs:
            freqs.append(f)
        else:
            return f
        if i == len(sequence) - 1:
            i = 0
        else:
            i = i + 1


def part2test() -> None:
    # test input
    testinput_sequence = [1, -2, 3, 1]
    test_output = find_repeatedfreq(testinput_sequence)
    assert (test_output == 2)

    assert (find_repeatedfreq([+1, -1]) == 0)
    assert (find_repeatedfreq([+3, +3, +4, -2, -4]) == 10)
    assert (find_repeatedfreq([-6, +3, +8, +5, -6]) == 5)
    assert (find_repeatedfreq([+7, +7, -2, -7, -4]) == 14)
    print("tests passed")


def part2(myinput: str) -> None:
    myinput_sequence = input_to_sequence(MYINPUT)
    result = find_repeatedfreq(myinput_sequence)
    print("answer:" + str(result))

###############
# Main
###############


if __name__ == "__main__":

    # my input
    with open('data/day1') as f:
        MYINPUT = f.read()

    print("Part 1:")
    part1test()
    part1(MYINPUT)

    print("Part 2:")
    part2test()
    part2(MYINPUT)
