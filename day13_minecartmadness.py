import numpy as np
import array2gif as gif
import skimage.transform
import random
import time


class Cart():

    def __init__(self, posx: int, posy: int, heading: str):
        self.x = posx
        self.y = posy
        self.heading = heading  # N,E,S,W
        self.decision = 0  # 0=left 1=strait 2=right
        self.color = Cart.generate_color()
        self.crashed = False

    @staticmethod
    def generate_color():
        return (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

    def __repr__(self):
        if self.heading == 'N':
            rep = "^"
        elif self.heading == 'E':
            rep = ">"
        elif self.heading == 'S':
            rep = "v"
        elif self.heading == 'W':
            rep = "<"
        return "{} [{} {}]".format(rep, self.x, self.y)

    def turn(self, turn_type):
        """
        Turns the cart in a new direction for a given corner type
        or intersection ahead of the cart
        """

        map_corner = {
            '\\': {'N': 'W', 'S': 'E', 'E': 'S','W': 'N'},
            '/' : {'N': 'E', 'S': 'W', 'E': 'N','W': 'S'}
        }
        map_intersection = {
            0: {'N': 'W', 'E': 'N', 'S': 'E', 'W': 'S'},
            1: {'N': 'N', 'E': 'E', 'S': 'S', 'W': 'W'},
            2: {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
        }

        if turn_type in ['/', '\\']:
            new_heading = map_corner[turn_type][self.heading]
            self.heading = new_heading
        elif turn_type == '+':
            new_heading = map_intersection[self.decision][self.heading]
            self.heading = new_heading
            self.decision += 1
            if self.decision == 3:
                self.decision = 0
        elif turn_type == ' ':
            print("off track!")

    def step(self, nxt):  # , surroundings):
        """
        Move one step depending on 'around',
        which is the area around the cart
        e.g.
            # # #
            # > #
            # # #
        """
        if self.heading == 'N':
            self.y += - 1
        elif self.heading == 'E':
            self.x += 1
        elif self.heading == 'S':
            self.y += 1
        elif self.heading == 'W':
            self.x += -1

        self.turn(nxt)


class Track():

    def __init__(self, layout: str):
        self.layout = layout
        self.shape = None
        self.carts = []
        self.history = {}
        self.t = 0
        self.frames = []

    def __repr__(self):
        return "\n".join([r for r in self.layout])

    def setup(self):
        rows = self.layout.split("\n")
        self.shape = (len(rows[0]), len(rows))
        for y, row in enumerate(rows):
            for x, point in enumerate(row):
                if not (point == " " or point == "\n"):
                    if point == "^":
                        self.carts.append(Cart(x, y, heading='N'))
                    elif point == ">":
                        self.carts.append(Cart(x, y, heading='E'))
                    elif point == "v":
                        self.carts.append(Cart(x, y, heading='S'))
                    elif point == "<":
                        self.carts.append(Cart(x, y, heading='W'))
        self.layout = rows
        self.layout = [
            r.replace('>', '-').replace('<','-') \
             .replace('^', '|').replace('v', '|')
            for r in rows]

    def tick(self):
        self.carts.sort(key=lambda c: (c.y, c.x))
        for cart in self.carts:
            if cart.heading == 'N':
                cart.step(nxt=self.layout[cart.y-1][cart.x])
            elif cart.heading == 'E':
                cart.step(nxt=self.layout[cart.y][cart.x+1])
            elif cart.heading == 'S':
                cart.step(nxt=self.layout[cart.y+1][cart.x])
            elif cart.heading == 'W':
                cart.step(nxt=self.layout[cart.y][cart.x-1])

            newpos = (cart.x, cart.y)
            self.history[newpos] = cart.color
            for cart2 in self.carts:
                if not cart == cart2:
                    if newpos == (cart2.x, cart2.y):
                        print("Crash! @ {}".format(newpos))
                        cart.crashed = True
                        cart2.crashed = True
        for cart in self.carts:
            if cart.crashed:
                print(str(cart) + "-> crashed")
            else:
                pass
                #print(cart)
        self.carts = [c for c in self.carts if not c.crashed]
        self.make_frame()
        self.t += 1

    def make_frame(self):
        # reset = '\u001b[0m'
        height = self.shape[1]
        width = self.shape[0]
        image = np.zeros((height, width, 3))

        carts_d = set()
        for cart in self.carts:
            x = cart.x
            y = cart.y
            image[y, x] = cart.color
            carts_d.add((x, y))
            self.history[x, y] = cart.color

        for y in range(height):
            for x in range(width):
                if (x, y) not in carts_d:
                    if (x, y) in self.history:
                        color = self.history[(x, y)]
                        image[y, x, :] = color

        self.frames.append(image)


testtrack = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/  """

# my input
with open('data/day13') as f:
    MYINPUT = f.read()


t = Track(MYINPUT)
t.setup()

while len(t.carts) > 1:
    t.tick()
    #time.sleep(0.1)

print(t.carts)

gif.write_gif(t.frames, 'day13.gif', fps=20)
