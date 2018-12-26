import re
from typing import Set, Dict


def parse_input(inp: str) -> Dict:
    re_nums = re.compile(r"[0-9]+")
    re_wi = re.compile(r"\(.+\)")
    re_at = re.compile(r"(\w+) damage")

    groups = []
    for team in inp.split("\n\n"):
        tname = team.strip().splitlines()[0].lower().replace(
            " ", "").replace(":", "")
        for line in team.strip().splitlines()[1:]:
            weaknesses = set()
            immunities = set()
            nums = re.findall(pattern=re_nums, string=line)
            nunits, hp, ad, initiative = (int(n) for n in nums)
            attack = re.findall(pattern=re_at, string=line)[0]
            try:
                weaknesses_and_immunities = re.findall(
                    pattern=re_wi, string=line)[0]
            except IndexError:
                pass
            else:
                for prop in weaknesses_and_immunities.lstrip("(").rstrip(")").split("; "):
                    p, types = prop.split(" to ")
                    if p == 'weak':
                        for t in types.split(","):
                            weaknesses.add(t.strip())
                    if p == 'immune':
                        for t in types.split(","):
                            immunities.add(t.strip())

            groups.append(Group(tname, nunits, hp, ad, initiative,
                                attack, weaknesses, immunities))

    return groups


class Group():
    def __init__(self, team: str, units: int,  hitpoints: int,
                 attack_damage: int, initiative: int, attack_type: str,
                 weaknesses: Set[str], immunities: Set[str]):
        self.team = team
        self.units = units
        self.hp = hitpoints
        self.dmg = attack_damage
        self.init = initiative
        self.attack = attack_type
        self.weaknesses = weaknesses
        self.immunities = immunities

    def __eq__(self, other):
        return (self is other
                or (type(self) == type(other)
                    and vars(self) == vars(other)))

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(tuple(sorted(vars(self).items())))

    def __repr__(self):
        return '{name}({values})'.format(
            name=type(self).__name__,
            values=', '.join(map(repr, vars(self).values())))

    @property
    def power(self):
        return self.units * self.dmg

    def possible_damage(self, target):
        base_dmg = self.power
        if self.attack in target.weaknesses:
            # print("target is weak")
            return 2*base_dmg
        if self.attack in target.immunities:
            # print("target is immune")
            return 0
        return base_dmg

    def defend(self, dmg):
        killed = dmg // self.hp
        self.units = self.units - killed
        if self.units <= 0:
            self.units = 0
        return killed


def battle(groups, boost=0):

    newgroups = []
    # boost
    for g in groups:
        if g.team == "immunesystem":
            newg = Group(g.team, g.units, g.hp, g.dmg + boost,
                         g.init, g.attack, g.weaknesses, g.immunities)
            newgroups.append(newg)
        else:
            newgroups.append(g)

    groups = newgroups

    while len(set(g.team for g in groups)) > 1:
        # choosing targets
        fights = []  # (attacker, defender)

        for attacker in sorted(groups, key=lambda x: (x.power, x.init), reverse=True):
            # choose target to which the group can deal the most damage
            # defending groups can only be chosen as a target by one attacking group
            defenders = [f[1] for f in fights]
            possible_targets = [g for g in groups
                                if not g.team == attacker.team
                                and g not in defenders]
            # (tie: most effective power, most initiative)
            if possible_targets:
                chosen_target = max(possible_targets,
                                    key=lambda t: (attacker.possible_damage(t),
                                                   t.power,
                                                   t.init))
                # only if damage is possible
                if attacker.possible_damage(chosen_target) > 0:
                    fights.append((attacker, chosen_target))

        # attacking
        # in order of decreasing initiative, each group deals damage
        fights = sorted(fights, key=lambda x: x[0].init, reverse=True)

        killcount = 0
        for fight in fights:
            attacker, defender = fight
            dmg = attacker.possible_damage(defender)
            killcount += defender.defend(dmg)

        # remove groups with zero units
        groups = [g for g in groups if g.units > 0]

       # if killcount == 0:
       #     print("stalemate")
       #     return("stalemate", "stalemate")
    winner = groups[0].team
    units_left = sum([g.units for g in groups])
    return winner, units_left


example = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""

myinput = open("data/day24", "r").read()

groups = parse_input(myinput)

boost = 0
while True:
    print("boost: " + str(boost))
    winner, left = battle(groups, boost)
    print("{} wins".format(winner))
    print("{} units left".format(left))
    if winner == "immunesystem":
        break
    boost += 1
