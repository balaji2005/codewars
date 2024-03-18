import random
import math

from numpy import sign

name = "scriptblue"


def moveTo(x, y, Pirate):
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return 0
    if position[0] == x:
        return (position[1] < y) * 2 + 1
    if position[1] == y:
        return (position[0] > x) * 2 + 2
    if random.randint(1, 2) == 1:
        return (position[0] > x) * 2 + 2
    else:
        return (position[1] < y) * 2 + 1

pirate_pos = dict()
pirate_goal = dict()
island_pos = dict()

# Get the closest n pirates to a given position
def closest_n_pirates(x, y, n, team):
    pirates = pirate_pos.keys()
    pirates.sort(key=lambda p: abs(p.getPosition()[0] - x) + abs(p.getPosition()[1] - y))

def ActPirate(pirate):
    global pirate_pos
    id = pirate.getID()
    pos = pirate.getPosition()
    pirate_pos[id] = (pos[0], pos[1])
    pirate.setSignal(f"{id},{pos[0]},{pos[1]}")
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]
    x, y = pirate.getPosition()
    # pirate.setSignal("")
    s = pirate.trackPlayers()
    
    if (
        (up == "island1" and s[0] != "myCaptured")
        or (up == "island2" and s[1] != "myCaptured")
        or (up == "island3" and s[2] != "myCaptured")
    ):
        s = up[-1] + str(x) + "," + str(y - 1)
        pirate.setTeamSignal(s)

    if (
        (down == "island1" and s[0] != "myCaptured")
        or (down == "island2" and s[1] != "myCaptured")
        or (down == "island3" and s[2] != "myCaptured")
    ):
        s = down[-1] + str(x) + "," + str(y + 1)
        pirate.setTeamSignal(s)

    if (
        (left == "island1" and s[0] != "myCaptured")
        or (left == "island2" and s[1] != "myCaptured")
        or (left == "island3" and s[2] != "myCaptured")
    ):
        s = left[-1] + str(x - 1) + "," + str(y)
        pirate.setTeamSignal(s)

    if (
        (right == "island1" and s[0] != "myCaptured")
        or (right == "island2" and s[1] != "myCaptured")
        or (right == "island3" and s[2] != "myCaptured")
    ):
        s = right[-1] + str(x + 1) + "," + str(y)
        pirate.setTeamSignal(s)
    # print(pirate.getTeamSignal())
    if pirate.getTeamSignal() != "":
        s = pirate.getTeamSignal()
        l = s.split(",")
        x = int(l[0][1:])
        y = int(l[1])
        
        return moveTo(x, y, pirate)

    else:
        return random.randint(1, 4)


def ActTeam(team):
    pirates = []
    for signal in team.getListOfSignals():
        if signal == "":
            continue
        signal = signal.split(",")
        # print(signal)
        id = signal[0]
        x = signal[1]
        y = signal[2]
        pirates.append((id, x, y))
        pirate_pos[id] = (x, y)
    keys = list(pirate_pos.keys())
    i = 0
    while i < len(keys):
        if keys[i] not in [p[0] for p in pirates]:
            del pirate_pos[keys[i]]
            i -= 1  
        i += 1
        keys = list(pirate_pos.keys())
    for pirate in pirate_pos.keys():
        if pirate not in [p[0] for p in pirates]:
            del pirate_pos[pirate]
    
    # print(len(pirate_pos))
    print(pirate_pos)
    l = team.trackPlayers()
    s = team.getTeamSignal()

    team.buildWalls(1)
    team.buildWalls(2)
    team.buildWalls(3)
    # print(team.getTeamSignal())
    # print(team.trackPlayers())
    if s:
        island_no = int(s[0])
        signal = l[island_no - 1]
        if signal == "myCaptured":
            team.setTeamSignal("")
