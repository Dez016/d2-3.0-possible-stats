import numpy as np
import csv
from interpreter import convert

#health, melee, grenade, supe, clas, weapons 

def fitLegArmor(request):
    requested = np.array(request).astype(int)

    print(requested)

    adjusted = requested
    lenience = 25+50

    possibilities = []
    padding = []

    combos = []
    legend = []

    with open('5pc.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            combos.append(row)

    npos = np.array(combos)
    stats = npos[:, :6].astype(int)
    legend = npos[:, -5:]

    print(legend)

    for i in range(len(stats)):
        stats[i] = stats[i]-adjusted

    stats = np.clip(stats, None, 0)

    print(stats)
    
    for i in range(len(stats)):
        if (-(np.sum(stats[i])) < lenience):
            
            split = [term.split('/') for term in legend[i]]
            #print(split)
            output = [0] * 36

            for j in range(len(split)):
                index = (int(split[-1-j][0])-1) * 6 + int(split[-1-j][1]) - 1 #I THINK THIS INDEX WORKS
                #print(split[-1-j])
                #print(index)
                output[index] = output[index] + 1
            
            if (not (output in possibilities)):
                possibilities.append(output)
                padding.append(-stats[i])

    print(possibilities)
    return possibilities, padding
