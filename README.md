Links
====

* (Scatterplot of results)[http://www.maurits.vdschee.nl/scatterplot/]
* (AoC Subreddit)[https://www.reddit.com/r/adventofcode]

Day 1
======

Part 1 was easy, probably a little overkill with separate functions part1test() and part1(). But I think this may be a good structure to get used to for future puzzles.

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

Part 1:
---------
Compute a checksum for a list of box IDs from the following rules:
1. a = number of IDs that have exactly _two_ of any letter
2. b = number of IDs that have exactly _three_ of any letter
3. checksum = a * b

For Part 1, I chose to use collections.Counter and iterate over the resulting dictionary. With at most 26 items to evaluate, this should be pretty quick. The checksum() function then simply sums the number of _True_s for two_of_any and three_of_any separately and finally multiplies them together.

```python
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
```

Part 2:
---------
Find the two correct box IDs, which are identified by the fact that their IDs differ by exactly one character at the same position in both box ID strings. This differing character needs to be removed to get the correct answer.

Assuming the IDs all have the same length, one approach would be to remove the same character (by position) in turn in all of the IDs and then check if any two are the same. 

```python
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
```

I'm actually pretty happy with this solution.. At least I was not able to find one I liked better on the AoC Solution Megathread... :)

One interesting approach from there by u/CFD999 for Part 2 looks like:
```python
print((lambda strs: (lambda a,b: "".join([a[i] for i in range(len(a)) if a[i] == b[i]]))(*[(l1.strip(),l2.strip()) for l1 in strs for l2 in strs if l1 != l2 and sum(1 for i in range(len(l1)-1) if l1[i] != l2[i]) < 2][0]))(open('inp', 'r').readlines()))
```