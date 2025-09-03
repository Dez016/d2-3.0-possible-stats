import numpy as np
import pyarrow
import csv
import os
from interpreter import convert
import pandas as pd

#health, melee, grenade, supe, clas, weapons 

def fitLegArmor(request):
    requested = np.array(request).astype(int)

    print(requested)

    adjusted = requested
    lenience = 25+50

    possibilities = []
    padding = []

    combos = []

    if os.path.exists('5pc.feather'):
        combos = pd.read_feather('5pc.feather')
        print("exists")
    else:
        dtype = {f'col{i}': int for i in range(1, 6)}
        dtype.update({f'col{i}': float for i in range(7, 11)})
        combos = pd.read_table('5pc_culled.csv', sep=',', header=None, dtype = dtype)

        combos.to_feather('5pc.feather')

    npos = combos.to_numpy()
    
    stats = npos[:, :6].astype(int)
    legend = npos[:, -5:].tolist()

    # print(stats)
    # #print(legend)

    stats = stats-adjusted

    stats = np.clip(stats, None, 0)

    
    sums = -np.sum(stats, axis = 1)

    valid = np.where(lenience >= sums)[0]\

    for i in valid: 
        output = [0] * 36

        split = [term.split('/') for term in legend[i]]

        for j in range(len(split)):
            index = (int(split[j][0])-1) * 6 + int(split[j][1]) - 1 #I THINK THIS INDEX WORKS
            output[index] = output[index] + 1

        possibilities.append(output)  
        padding.append(-stats[i])

    print(possibilities)
    return possibilities, padding


fitLegArmor([0,80,200,125,70,0])