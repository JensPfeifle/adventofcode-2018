from collections import defaultdict
from collections import deque
# INPUT:
# 419 players; last marble is worth 71052 points
nplayers = 419
last_score = 71052

def play_game(nplayers, lastmarble):
    marbles = range(2,lastmarble+1)
    players = defaultdict(list)
    circle =[0,1]

    current_id = 0
    next_id = current_id +1

    current_player = 2  # marble 1 already played
    for m in marbles:
        if m % 23 == 0:
            #print("player {} takes {}".format(current_player, m))
            players[current_player].append(m)
            p7_idx = (current_id - 7) % len(circle)
            #del circle[p7_idx]
            #print("player {} removes  {}".format(current_player, circle[p7_idx]))
            players[current_player].append(circle[p7_idx])
            circle.remove(circle[p7_idx])
            current_id = p7_idx
            next_id = current_id + 2
        else:
            #print("play marble {}".format(m))
            #print("pn_idx = " + str(pn_idx))
            circle.insert(next_id, m)
            #print(circle)
            current_id = next_id
            next_id = (current_id + 2 ) % len(circle)

        current_player = current_player + 1 if current_player < nplayers else 1

    playerscores = [(p,sum(players[p])) for p in players.keys()]
    player_and_max_score = max(playerscores,key=lambda t: t[1])
    return player_and_max_score


# solution with deque by /u/marcusandrews
def play_game_deque(max_players, last_marble):
    scores = defaultdict(int)
    circle = deque([0])

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % max_players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores.values()) if scores else 0


# test
assert play_game(9,25) == (5,32) 
assert play_game(10,1618)[1] == 8317 
assert play_game(13,7999)[1] == 146373
assert play_game(17,1104)[1] == 2764 
assert play_game(21,6111)[1] == 54718 
assert play_game(30,5807)[1] == 37305 

# part1
print(play_game_deque(419,last_marble = 71052*100))