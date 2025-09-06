

tert_dict = {
    "Spirit of the Star-Eater": ["s", "h"], 
    "Spirit of Synthoceps": ["m","h","c"], 
    "Spirit of Verity": ["g","s","m"], 

    "Spirit of Vesper": ["c","w","h"],
    "Spirit of Harmony": ["s","w"], 
    "Spirit of Starfire": ["g","s","w"],
    "Spirit of the Swarm": ["g","m"],
    "Spirit of the Claw": ["m","h","c"],

    "Spirit of the Cyrtarachne": ["g","h"],
    "Spirit of the Gyrfalcon": ["w","c","m"], 
    "Spirit of the Liar": ["m","h","c"],
    "Spirit of the Wormhusk": ["c", "m"], #drag husk
    "Spirit of the Coyote": ["c","m"],

    "Spirit of Contact": ["m","h","g"],
    "Spirit of Scars": ["h","w"],
    "Spirit of the Horn": ["c","g"],
    "Spirit of Alpha Lupi": ["c","h"],
    "Spirit of the Armamentarium": ["c","h"] 
}

arch_dict = {
    "Spirit of the Assassin": 2,
    "Spirit of Inmost Light": 4,
    "Spirit of the Ophidian": 6,

    "Spirit of the Stag": 1, 
    "Spirit of the Filament": 5,
    "Spirit of the Necrotic": 2,
    "Spirit of Osmiomancy": 3, 
    "Spirit of Apotheosis": 4,
    
    "Spirit of the Dragon": 5, 
    "Spirit of Galanor": 4, 
    "Spirit of the Foetracer": 6, 
    "Spirit of Caliban": 2, 
    "Spirit of Renewal": 3, 

    "Spirit of Severance": 2, 
    "Spirit of Hoarfrost": 5, 
    "Spirit of the Eternal Warrior": 4,
    "Spirit of the Abeyant": 5,
    "Spirit of the Bear": 3
}

def set_vals(stats, stat1, val1, stat2, val2):
    stats[stat1] = val1
    stats[stat2] = val2

def classitemtostats(first, second):
        
    stats = {
    "h": 5,
    "m": 5,
    "g": 5,
    "s": 5,
    "c": 5,
    "w": 5
    }

    arch_case = {
    1: lambda: set_vals(stats, "h", 30, "c", 20),
    2: lambda: set_vals(stats,"m", 30, "h", 20),
    3: lambda: set_vals(stats,"g", 30, "s", 20),
    4: lambda: set_vals(stats,"s", 30, "m", 20),
    5: lambda: set_vals(stats,"c", 30, "w", 20),
    6: lambda: set_vals(stats,"w", 30, "g", 20),
    }

    unknown = True

    arch_case[arch_dict.get(first)]() #dictionary on 1st spirit -> dictionary w/ lambda function

    terts = tert_dict.get(second) #dict on 2nd spirit

    # place tertiary in unused spot by priority (order in array)
    for i in terts: 
        print(stats.get(i))
        if (int(stats.get(i)) == 5):
            stats[i] = 13
            unknown = False
            break

    if unknown: 
        return "unknown combo. if you have this class item combo please dm its stat split to dezedz on discord"
    else:
        return list(stats.values())

