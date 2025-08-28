import csv
import numpy as np

#health, melee, grenade, supe, clas, weapons 

rows = []

    #open armor stats sheet
with open('combo table - armor.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        rows.append(row)

    #open armor archetypes sheet (ex. 6/1)
archetypes = []
with open('combo table - armor - Copy.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        archetypes.append(row)
print(archetypes)
#print(rows)

exos = []
#opening exotic armor rolls
with open('exoticrolls.csv', newline = '') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        exos.append(row)

nprows = np.array(rows)
nprows = nprows.astype(int)
exotics = np.array(exos).astype(int)

#print(nprows[0]+nprows[0])
output = np.array([])

    #loop ts
with open('4pcexo.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in range(len(rows)):
        for j in range(len(rows)):
            for k in range(len(rows)):
                for l in range(len(rows)):
                    for e in range(len(rows)):
                        combo = np.append(exotics[e] + nprows[i]+nprows[j]+nprows[k]+nprows[l], archetypes[e] + archetypes[i]+archetypes[j]+archetypes[k]+archetypes[l])
                        print(combo)
                        writer.writerow(combo)

