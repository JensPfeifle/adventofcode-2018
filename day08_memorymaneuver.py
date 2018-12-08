from typing import Set, DefaultDict, Tuple, List
import collections

Node = collections.namedtuple('Node', 
    ['nchildren', 'nmeta', 'children', 'metadata', 'lchildren'])


def parse(data):
    # print("--------")
    header = data[:2]
    data = data[2:]
    #print("{} {}".format(header, data))

    nchildren, nmeta = header

    totals = 0
    values = []  # scores for children of this node

    for n in range(nchildren):
        # print("child{}".format(n))
        total, value, data = parse(data)
        totals += total
        values.append(value)

    if nchildren == 0:
        total = sum(data[:nmeta])
        value = total
        restdata = data[nmeta:]
        return total, value, restdata
    else:
        totals += sum(data[:nmeta])
        value = 0
        for m in data[:nmeta]:
            if m > 0 and m <= nchildren:
                value += values[m - 1]  # index starts at 0
        restdata = data[nmeta:]
        return totals, value, restdata


def tests():
    testinput = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    testinput = [int(i) for i in testinput.split()]
    total, value, restdata = parse(testinput)
    assert len(restdata) == 0
    assert total == 138, print("total is {}".format(total))
    assert value == 66, print("root value is {}".format(value))


if __name__ == "__main__":

    tests()

    with open('data/day8', 'r') as f:
        myinput = f.read().strip()
    myinput = [int(i) for i in myinput.split()]

    print("Part1")
    total, value, _ = parse(myinput)
    print(total)
    print("Part2")
    print(value)
