
def convert(archArray):
    archetypes = []
    for i in range(len(archArray)):
        if int(archArray[i]) > 0:
            tertin = (i)% 6 + 1
            archin = (i - tertin + 1)/6 + 1

            #print(tertin, archin)

            switchtert = {
                1: "Health",
                2: "Melee",
                3: "Grenade",
                4: "Super",
                5: "Class",
                6: "Weapons"
            }

            switcharch = {
                1: "Bulwark",
                2: "Brawler",
                3: "Grenadier",
                4: "Paragon",
                5: "Specialist",
                6: "Gunner"
            }

            archetypes.append(str(archArray[i]) + " " + switcharch.get(archin, "UNKNOWN") + " " + switchtert.get(tertin, "UNKNOWN"))
    return archetypes

def convertExo(archArray):

    switchtert = {
        1: "Health",
        2: "Melee",
        3: "Grenade",
        4: "Super",
        5: "Class",
        6: "Weapons"
    }

    switcharch = {
        1: "Bulwark",
        2: "Brawler",
        3: "Grenadier",
        4: "Paragon",
        5: "Specialist",
        6: "Gunner"
    }
    
    archetypes = []
    
    #exotic part: simply encoded both numbers in the exotic since there's only one (order doesnt matter)
    exoin = archArray[36]
    tertexo = (exoin)% 6 + 1
    archexo = (exoin - tertexo + 1)/6 + 1

    archetypes.append("Exotic: " + switcharch.get(archexo, "UNKNOWN") + " " + switchtert.get(tertexo, "UNKNOWN"))

    for i in range(len(archArray) - 1): #final term reserved for exotic armor piece
        if archArray[i] > 0:
            tertin = (i)% 6 + 1
            archin = (i - tertin + 1)/6 + 1

            print(tertin, archin, exoin)

            archetypes.append(str(archArray[i]) + " " + switcharch.get(archin, "UNKNOWN") + " " + switchtert.get(tertin, "UNKNOWN"))
    return archetypes




#switchtert = {
#        1: "Health",
##        2: "Melee",
##        3: "Grenade",
 #       4: "Super",
 #       5: "Class",
 #       6: "Weapons"
 ##   }#

#switcharch = {
###        1: "Bulwark",
   #     2: "Brawler",
 #       3: "Grenadier",
 ##       5: "Specialist",
 ##       6: "Gunner"
  # }
#print(convertExo([0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0,13]))

#for i in range(35):
#    tertexo = (i) % 6 + 1
#    archexo = (i - tertexo + 1)/6 +1
#
#    print(archexo, tertexo)
#   print("Exotic: " + switcharch.get(archexo, "UNKNOWN") + " " + switchtert.get(tertexo, "UNKNOWN"))
