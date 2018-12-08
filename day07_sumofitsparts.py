from collections import defaultdict
from typing import Set, DefaultDict
from copy import copy

def parse_steps(myinput: list) -> (Set, DefaultDict):
    steps = set()
    prereqs = defaultdict(list)

    for inp in myinput:
        step1 = inp.split()[1]
        step2 = inp.split()[7]
        steps.add(step1)
        steps.add(step2)
        prereqs[step2].append(step1)

    return steps, prereqs


def step_order(steps: Set, prereqs: DefaultDict) -> str:
    steps = steps.copy()
    preqs = copy(prereqs)
    steps_taken = ''

    while steps:
        steps_available = [s for s in steps if s not in preqs.keys()]

        assert len(steps_available) > 0

        #print("availale steps: {}".format(steps_available))
        next_step = sorted(steps_available)[0]

        #print("taking step: {}".format(next_step))
        steps_taken += next_step
        # completed - remove from steps
        steps.remove(next_step)

        # remove from prereqs
        tmp = copy(preqs)
        for s in preqs.keys():
            if next_step in preqs[s]:
                preqs[s].remove(next_step)
            if len(preqs[s]) == 0:
                del tmp[s]
        preqs = tmp

    return steps_taken


def total_time(steps: Set, prereqs: DefaultDict, nworkers: int):
    steps = steps.copy()
    preqs = copy(prereqs)
    completed = set()
    workers = {}
    for n in range(nworkers):
        workers[n] = ('.', 0)  # [('A', 60)]
    print(workers)
    t = 0
    while steps or len([task for task in workers.values() if not task[0] == '.']) > 0:
        steps_available = sorted([s for s in steps if s not in preqs.keys()])
        #print("steps: {}".format(steps))
        #print("prereqs: {}".format(prereqs))
        #print("available steps: {}".format(steps_available))

        for n in range(len(workers)):
            step, remaining_time = workers[n]
            if step == '.':                 # worker idle
                #print("worker" + str(n) + " idle")
                if steps_available: 
                    #print("worker" + str(n) + " gets job")
                    next_step = steps_available.pop(0)
                    workers[n] = (next_step, next_step_durations[next_step]-1)
                    steps.remove(next_step)
            elif remaining_time == 0:       # step completed in this t
                #print("worker" + str(n) + " finished")
                completed.add(step)
                tmp = preqs.copy()
                for s in preqs.keys():
                    if step in preqs[s]:
                        preqs[s].remove(step)
                    if len(preqs[s]) == 0:
                        del tmp[s]
                preqs = tmp
                steps_available = sorted([s for s in steps if s not in preqs.keys()])
                #print("availale steps: {}".format(steps_available))
                if steps_available:
                    next_step = steps_available.pop(0)
                    workers[n] = (next_step, next_step_durations[next_step]-1)
                    steps.remove(next_step)
                else:
                    workers[n] = ('.', 0)
            else:                           # working on a task
                #print("worker" + str(n) + " working")
                workers[n] = (step, remaining_time - 1)

        print("{}\t{}".format(t, workers))
        #print("\t{}".format(completed))
        t+= 1
    return t-1


def tests():
    testinput = """
    Step C must be finished before step A can begin.
    Step C must be finished before step F can begin.
    Step A must be finished before step B can begin.
    Step A must be finished before step D can begin.
    Step B must be finished before step E can begin.
    Step D must be finished before step E can begin.
    Step F must be finished before step E can begin.
    """
    steps, prereqs = parse_steps(testinput.strip().split("\n"))
    print(steps)
    assert step_order(steps, prereqs) == 'CABDFE'
    steps, prereqs = parse_steps(testinput.strip().split("\n"))
    assert total_time(steps, prereqs, nworkers=2) == 15


if __name__ == "__main__":
        
    next_step_durations = dict(zip([chr(i).upper()
                                    for i in range(97, 97+26)], range(1, 1+26)))
    tests()

    with open('data/day7', 'r') as f:
        myinput = f.read().strip().split("\n")

    next_step_durations = dict(zip([chr(i).upper()
                                for i in range(97, 97+26)], range(61, 61+26)))

    print("Part1")
    steps, prereqs = parse_steps(myinput)
    print(step_order(steps, prereqs))

    print("Part2")
    steps, prereqs = parse_steps(myinput)
    print(total_time(steps, prereqs, nworkers=5))