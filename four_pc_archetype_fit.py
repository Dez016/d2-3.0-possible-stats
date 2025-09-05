import numpy as np
import pyarrow
import csv
import os
import pandas as pd

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

    if os.path.exists('4pc.feather'):
        combos = pd.read_feather('4pc.feather')
        print("exists")
    else:
        dtype = {f'col{i}': int for i in range(1, 6)}
        dtype.update({f'col{i}': float for i in range(7, 11)})
        combos = pd.read_table('4pc_culled.csv', sep=',', header=None, dtype = dtype)

        combos.to_feather('4pc.feather')

    npos = np.array(combos)
    stats = npos[:, :6].astype(int)
    legend = npos[:, -4:]

    print(stats)

    stats = stats - adjusted
    stats = np.clip(stats, None, 0)

    sums = -np.sum(stats, axis = 1)

    valid = np.where(lenience >= sums)[0]

    for i in valid: 
        output = [0] * 36

        split = [term.split('/') for term in legend[i]]

        for j in range(len(split)):
            index = (int(split[j][0])-1) * 6 + int(split[j][1]) - 1 #I THINK THIS INDEX WORKS
            output[index] = output[index] + 1

        possibilities.append(output)  
        padding.append(-stats[i])

    #print(possibilities)
    return possibilities, padding



#fitStats([0,70,170,0,70,0], [0,20,5,30,5,5])