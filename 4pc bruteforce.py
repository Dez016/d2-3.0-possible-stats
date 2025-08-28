import csv
import numpy as np

#health, melee, grenade, supe, clas, weapons 

rows = []

    #open archetypes sheet 
with open('combo table - armor.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        rows.append(row)

archetypes = []
with open('combo table - armor - Copy.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        archetypes.append(row)
print(archetypes)
#print(rows)

nprows = np.array(rows)
nprows = nprows.astype(int)

#print(nprows[0]+nprows[0])
output = np.array([])

    #loop ts
with open('4pc.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in range(len(rows)):
        for j in range(len(rows)):
            for k in range(len(rows)):
                for l in range(len(rows)):
                    combo = np.append(nprows[i]+nprows[j]+nprows[k]+nprows[l], archetypes[i]+archetypes[j]+archetypes[k]+archetypes[l])
                    print(combo)
                    writer.writerow(combo)

