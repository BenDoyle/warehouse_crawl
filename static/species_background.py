from parsers.common import write_rows_to_csv
from core.utils import add_key
import os

SPECIES = [
    ['Barachi', 'Ba'],
    ['Centaur', 'Ce'],
    ['Deep Dwarf', 'DD'],
    ['Deep Elf', 'DE'],
    ['Demigod', 'Dg'],
    ['Demonspawn', 'Ds'],
    ['Draconian', 'Dr'],
    ['Red Draconian', 'Dr'],
    ['White Draconian', 'Dr'],
    ['Green Draconian', 'Dr'],
    ['Yellow Draconian', 'Dr'],
    ['Grey Draconian', 'Dr'],
    ['Black Draconian', 'Dr'],
    ['Purple Draconian', 'Dr'],
    ['Pale Draconian', 'Dr'],
    ['Felid', 'Fe'],
    ['Formicid', 'Fo'],
    ['Gargoyle', 'Gr'],
    ['Ghoul', 'Gh'],
    ['Gnoll', 'Gn'],
    ['Halfling', 'Ha'],
    ['Hill Orc', 'HO'],
    ['Human', 'Hu'],
    ['Kobold', 'Ko'],
    ['Merfolk', 'Mf'],
    ['Minotaur', 'Mi'],
    ['Mummy', 'Mu'],
    ['Naga', 'Na'],
    ['Octopode', 'Op'],
    ['Ogre', 'Og'],
    ['Spriggan', 'Sp'],
    ['Tengu', 'Te'],
    ['Troll', 'Tr'],
    ['Vampire', 'Vp'],
    ['Vine Stalker', 'VS'],
]

BACKGROUNDS = [
    ['Warrior', 'Fighter', 'Fi'],
    ['Warrior', 'Gladiator', 'Gl'],
    ['Warrior', 'Monk', 'Mo'],
    ['Warrior', 'Hunter', 'Hu'],
    ['Warrior', 'Assassin', 'As'],
    ['Zealot', 'Berserker', 'Be'],
    ['Zealot', 'Abyssal Knight', 'AK'],
    ['Zealot', 'Chaos Knight', 'CK'],
    ['Warrior-mage', 'Skald', 'Sk'],
    ['Warrior-mage', 'Enchanter', 'En'],
    ['Warrior-mage', 'Transmuter', 'Tm'],
    ['Warrior-mage', 'Arcane Marksman', 'AM'],
    ['Warrior-mage', 'Warper', 'Wr'],
    ['Mage', 'Wizard', 'Wz'],
    ['Mage', 'Conjurer', 'Cj'],
    ['Mage', 'Summoner', 'Su'],
    ['Mage', 'Necromancer', 'Ne'],
    ['Mage', 'Fire Elementalist', 'FE'],
    ['Mage', 'Ice Elementalist', 'IE'],
    ['Mage', 'Air Elementalist', 'AE'],
    ['Mage', 'Earth Elementalist', 'EE'],
    ['Mage', 'Venom Mage', 'VM'],
]

def get_row(species, background):
    combined = '{} {}'.format(species[0], background[1])
    short_combined = species[1] + background[2]
    return [23, 23] + species + background + [combined, short_combined]

if __name__ == '__main__':
    rows = [
        get_row(species, background)
        for species in SPECIES
        for background in BACKGROUNDS
    ]

    file_name = 'data/static/species_background.csv'
    write_rows_to_csv(add_key(rows), file_name)
    print(file_name)
