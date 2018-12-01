Day 1
======

Part 1 was easy, probably a little overkill with separate functioons part1test() and part1(). But I think this may be a good structure to get used to for future puzzles.

First solution to part2 was very slow (1-2 minutes for my input):

```python
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
```

The final solution uses a set instead of a list (duh...) and itertools.cycle() and completes in about 0.1s:

``` python
def find_repeatedfreq_itertools(sequence: [], f=0) -> int:
    freqs = set([f])
    for df in itertools.cycle(sequence):
        f = f + df
        if f not in freqs:
            freqs.add(f)
        else:
            return f
```

Day 2
======