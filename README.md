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

Day 3
======

Went a little more for speed today, as I have some real work that needs to be done...so neither pretty nor efficient.
This was my initial approach for Part 2 was truly awful:
```python
def overlaps(c1: Tuple, c2: Tuple) -> bool:
    i1, x1, y1, w1, h1 = c1
    i2, x2, y2, w2, h2 = c2

    if i1 == i2:
        return False

    fabric = np.zeros((1000, 1000))
    fabric[x1:x1+w1, y1:y1+h1] += 1
    fabric[x2:x2+w2, y2:y2+h2] += 1

    if fabric.max() > 1:
        #print("{} and {} overlap".format(i1,i2))
        return True
    else:
        #print("{} and {} don't overlap".format(i1,i2))
        return False

def intact_claims(claims: [str]) -> [int]:
    intact = []
    for cli in claims:
        ovlps = 0
        cl1 = claim_to_slice(cli)
        for clj in claims:
            cl2 = claim_to_slice(clj)
            if overlaps(cl1, cl2):
                ovlps += 1
                break
                print(ovlps)
        if ovlps == 0:
            intact.append(cl1[0])  # index
    return intact
```

...but finally:
```python
def intact_claims(claims: [str]) -> [int]:
    intact = []
    fabric = np.zeros((1000, 1000))
    for claim in claims:
        i, x, y, w, h = claim_to_slice(claim)
        fabric[x:x+w, y:y+h] += 1

    for claim in claims:
        i, x, y, w, h  = claim_to_slice(claim)
        if np.all(fabric[x:x+w, y:y+h] == 1):
            intact.append(i)
    return intact
```

Once I realized I could go through each claim and check if any others overlap it (i.e. fabric[i,j] > 1) instead of comparing the areas of each claim with all others, everything got much simpler. The final code is simplified further.

Day 4
======
