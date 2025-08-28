import numpy as np
import csv

#health, melee, grenade, supe, clas, weapons 

def fitExoArmorStats(request):
    requested = np.array(request).astype(int)

    print(requested)

    adjusted = requested
    lenience = 20+50

    possibilities = []
    padding = []

    combos = []
    legend = []

    with open('4pcexo.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            combos.append(row)

    npos = np.array(combos)
    stats = npos[:, :6].astype(int)
    legend = npos[:, -5:]

    print(stats)

    for i in range(len(stats)):
        stats[i] = stats[i]-adjusted

    stats = np.clip(stats, None, 0)

    print(stats)
    
    for i in range(len(stats)):
        if (-(np.sum(stats[i])) < lenience):
            
            split = [term.split('/') for term in legend[i]]
            output = [0] * 37

            exo_arch = split[0]
            output[36] = (int(exo_arch[0])-1)*6 + int(exo_arch[1]) - 1 #SAME THING as BELOW

            for j in range(len(split)-1):
                index = (int(split[-1-j][0])-1) * 6 + int(split[-1-j][1]) - 1 #I THINK THIS INDEX WORKS
                print(split[-1-j])
                print(index)
                output[index] = output[index] + 1
            
            if (not (output in possibilities)):
                possibilities.append(output)
                padding.append(-stats[i])

    print(possibilities)
    return possibilities, padding


#fitExoArmorStats([0,70,170,0,70,0])