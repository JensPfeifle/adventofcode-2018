#!/usr/bin/python3
import time
from collections import defaultdict
from collections import Counter


def parse_records():

    total_sleeping = defaultdict(int)
    minutes_counter = defaultdict(Counter)

    # my input
    with open('data/day4') as f:
        records = f.read().splitlines()

        records.sort()
        fall_asleep_minute = 0

        for record in records:
            splitline = record.split()
            date = splitline[0][1:] 
            time = splitline[1][:-1]
            
            if 'begins shift' in record:
                guard = int(record.split()[3][1:])

            if 'falls asleep' in record:  # can asssume the hour is 00

                H = int(time.split(":")[0])
                M = int(time.split(":")[1])
                assert H == 0
                fall_asleep_minute = M

            if 'wakes up' in record:
                H = int(time.split(":")[0])
                M = int(time.split(":")[1])
                assert H == 0

                time_asleep = M - fall_asleep_minute
                assert time_asleep > 0
                #print("{} asleep from {} to {}".format(guard, fall_asleep_minute,M))
                cnt = Counter([i for i in range(fall_asleep_minute,M)])
                minutes_counter[guard].update(cnt)
                oldtotal = total_sleeping[guard]
                total_sleeping[guard] = oldtotal + time_asleep
    
    return total_sleeping, minutes_counter


# largest total sleeping

def part1():
    totals, minutes = parse_records()
    # dangerous? assumes max minute will be larger than max gid
    mins, gid = max([mins,gid] for gid, mins in totals.items())
    mostcommon = minutes[gid].most_common()[0][0]
    print("Sleepiest guard: {}".format(gid))
    print("Asleep for {} minutes".format(mins))
    print("Mostly during minute {}".format(mostcommon))

def part2():
    totals, minutes = parse_records()
    lst = [(gid, counter.most_common()[0]) for gid, counter in minutes.items()]
    print(lst)
    gid, (m, n) = max(lst, key=lambda x: x[1][1])
    print("Guard #{} was asleep {} times during minute {}".format(gid, n, m))
      #  print(gid, counter.most_common()[0])

if __name__ == "__main__":
    print("Part 1:")
    t0 = time.time()
    part1()
    print("time: " + str(time.time() - t0))
  
    
    print("Part 2:")
    t0 = time.time()
    part2()
    print("time: " + str(time.time() - t0))



