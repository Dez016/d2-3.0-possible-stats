from four_pc_archetype_fit import fitStats
from five_pc_exotic_fit import fitExoArmorStats
from interpreter import convert, convertExo

test = [0] * 36

for i in range(6):
    for j in range(6):
        index = ((int(i)+1)-1) * 6 + (int(j)+1) - 1
        test[index] = 1

        for k in range(len(test)):
            if (test[k] > 0):
                print("index: ", k)
                tertin = (k)% 6 + 1
                archin = (k - tertin + 1)/6 + 1
                print(archin)
                print(tertin)

#indices DO go from 0-36. arch -> index seems to work

#archetypes, fluff = fitStats([20,20,0,30,170,165], [5,5,5,13,30,20])
#for term in archetypes:
#
#    print(convert(term))

archetypes2, fluff2 = fitExoArmorStats([150,20,0,20,0,140])
print(archetypes2)
for term in archetypes2:
    print(convertExo(term))





#print(fitExoArmorStats[])
