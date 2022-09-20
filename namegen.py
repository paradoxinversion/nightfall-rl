import random

class NameGenerator():
    afab_names = []
    amab_names = []
    last_names = []
    initialized = False
    
    def load_names():
        print("Loading names for NameGenerator...")
        total_names = 0
    
        afab_names = open('gen_sources/names/first/afab.txt', 'r')
        afab_names_raw = afab_names.readlines()
        afab_names = []
        for name in afab_names_raw:
            afab_names.append(str.capitalize(name).strip())
        NameGenerator.afab_names = afab_names
        amab_names = open('gen_sources/names/first/amab.txt', 'r')
        amab_names_raw = amab_names.readlines()
        amab_names = []
        for name in amab_names_raw:
            amab_names.append(str.capitalize(name).strip())
        NameGenerator.amab_names = amab_names
        
        last_names = open('gen_sources/names/last.txt', 'r')
        last_names_raw = last_names.readlines()
        last_names = []
        for name in last_names_raw:
            last_names.append(str.capitalize(name).strip())
        NameGenerator.last_names = last_names

        total_names += len(last_names)
        NameGenerator.initialized = True
        print(f"Namegen loaded {total_names} names")
    
    def get_first_name(afab: bool = False):
        if NameGenerator.initialized == False:
            NameGenerator.load_names()
        if afab:
            return random.choice(NameGenerator.afab_names)
        else:
            return random.choice(NameGenerator.amab_names)

    def get_last_name():
        if NameGenerator.initialized == False:
            NameGenerator.load_names()
        return random.choice(NameGenerator.last_names)