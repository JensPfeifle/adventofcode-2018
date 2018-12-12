import numpy as np
from numba import jit
from typing import Dict


def powerlevels(serial_number):
    grid = np.zeros([300, 300], dtype=int)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            rack_id = i + 10
            power = rack_id * j
            power = power + serial_number
            power = power * rack_id
            if len(str(power)) > 3:
                power = int(str(power)[-3])
            else:
                power = 0
            power -= 5
            grid[i, j] = power
    return grid


squares = {}


@jit(nopython=True, parallel=True)
def para_incr_sum(power_levels, prev_sum: int, size: int, row: int, col: int):
    sum_power = prev_sum
    i = row
    j = col
    for k in range(col, col+size):
        sum_power += power_levels[k, col + size-1]
    for l in range(row, row + size):
        sum_power += power_levels[row+size-1, l]
    return sum_power


@jit(nopython=True, parallel=True)
def para_sum_squares(power_levels, size=3):
    sums = []  # square sums for this power level
    for i in range(0, power_levels.shape[0] - size+1):
        for j in range(0, power_levels.shape[1] - size+1):
            sum_power = 0
            for k in range(i, i+size):
                for l in range(j, j+size):
                    sum_power += power_levels[k, l]
            sums.append(sum_power)
    return sums


def cached_para_sum_squares(power_levels, size):
    print("size = {}".format(size))
    for i in range(0, power_levels.shape[0] - size+1):
        for j in range(0, power_levels.shape[1] - size+1):
            if (i, j, size-1) in squares.keys():
                # print("{},{} size {} found".format(i, j, size-1))
                prev_sum = squares[(i, j, size-1)]
                squares[(i, j, size)] = para_incr_sum(
                    power_levels, prev_sum, size, i, j)
            else:
                # print("{},{} size {} not found".format(i, j, size-1))
                sum_power = 0
                for k in range(i, i+size):
                    for l in range(j, j+size):
                        # print("+grid[{},{}]".format(k,l))

                        sum_power += power_levels[k, l]
                squares[(i, j, size)] = sum_power


def sum_squares(power_levels, size=3):
    print("size = {}".format(size))
    for i in range(0, power_levels.shape[0] - size+1):
        for j in range(0, power_levels.shape[1] - size+1):
            if (i, j, size-1) in squares.keys():
                # print("{},{} size {} found".format(i, j, size-1))
                sum_power = (squares[(i, j, size-1)]
                             + sum(power_levels[i+size-1, j:j+size])
                             + sum(power_levels[i:i+size - 1, j + size-1]))
                squares[(i, j, size)] = sum_power
            else:
                # print("{},{} size {} not found".format(i, j, size-1))
                sum_power = 0
                for k in range(i, i+size):
                    for l in range(j, j+size):
                        # print("+grid[{},{}]".format(k,l))

                        sum_power += power_levels[k, l]
                squares[(i, j, size)] = sum_power


assert powerlevels(57)[122, 79] == -5.0
assert powerlevels(39)[217, 196] == 0.0
assert powerlevels(71)[101, 153] == 4.0


def maxpower(sqs):
    return max([(sq, pw) for sq, pw in sqs.items()], key=lambda x: x[1])

##############
#   Tests
##############
# squares = {}
# for s in range(1, 20):
#    sum_squares(powerlevels(18), size=s)
# print(maxpower(squares))  # should be 90,269,16 with power 113
# squares = {}
# for s in range(1, 20):
#    sum_squares(powerlevels(42), size=s)
# print(maxpower(squares))  # should be 232,251,12 with power 119


print("Part1")
squares = {}
sum_squares(powerlevels(3214), size=3)
print(maxpower(squares))
print("Part2")
for s in range(1, 300):
    cached_para_sum_squares(powerlevels(3214), size=s)
print(maxpower(squares))  # should be 232,251,12 with power 119