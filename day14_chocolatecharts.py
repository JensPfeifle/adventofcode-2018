MY_INPUT = 765071

required_num_scores = MY_INPUT*10000
searchdigits = list(map(int,str(MY_INPUT)))
#required_num_scores = 2018
#searchdigits = list(int(s) for s in str('92510'))
#searchdigits = None

scores = [3, 7]
elf1 = 0
elf2 = 1
n = 0
while True:

    s1 = scores[elf1]
    s2 = scores[elf2]
    new_score = str(s1+s2)
    assert len(new_score) <= 2

    scores.append(int(new_score[0]))
    if len(new_score) > 1:
        scores.append(int(new_score[1]))
    
    num_scores = len(scores)
    elf1 = (elf1 + 1 + s1) % num_scores
    elf2 = (elf2 + 1 + s2) % num_scores

    if num_scores >= required_num_scores + 10:
        print("stopped after {} recepies".format(num_scores))
        break

    if searchdigits:
        if scores[-len(searchdigits):] == searchdigits:
            print("Part2")
            print("found {}".format(searchdigits))
            print(num_scores - len(searchdigits))
            break
        if scores[-len(searchdigits)-1:-1] == searchdigits:
            print("Part2")
            print("found {}".format(searchdigits))
            print(num_scores - len(searchdigits) - 1)
            break

    n += 1

print("Part1")
print(scores[-10:])


