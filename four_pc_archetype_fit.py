import numpy as np
import csv

#health, melee, grenade, supe, clas, weapons 

def fitStats(request, exoti):
    requested = np.array(request).astype(int)
    exotic = np.array(exoti).astype(int)

    print(requested)
    print(exotic)

    adjusted = np.clip((requested - exotic), 0, None)
    lenience = 20+50

    possibilities = []
    padding = []

    combos = []
    legend = []

    with open('4pc.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            combos.append(row)

    npos = np.array(combos)
    stats = npos[:, :6].astype(int)
    legend = npos[:, -4:]

    print(stats)

    for i in range(len(stats)):
        stats[i] = stats[i]-adjusted

    stats = np.clip(stats, None, 0)

    print(stats)
    
    for i in range(len(stats)):
        if (-(np.sum(stats[i])) < lenience):
            
            split = [term.split('/') for term in legend[i]]
            output = [0] * 36

            for roll in split:
                index = (int(roll[0])-1) * 6 + int(roll[1]) - 1
                output[index] = output[index] + 1
            
            if (not (output in possibilities)):
                possibilities.append(output)
                padding.append(-stats[i])
    print(possibilities)
    return possibilities, padding#


#fitStats([0,70,170,0,70,0], [0,20,5,30,5,5])