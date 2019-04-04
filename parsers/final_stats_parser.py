from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
import os
import glob
import re

def get_value(pattern, contents):
    match = re.search(pattern, contents)
    if match:
        return match.group(1)
    else:
        return None

def get_double(pattern, contents):
    match = re.search(pattern, contents)
    if match:
        return (match.group(1), match.group(2))
    else:
        return (None, None)

def get_positional(starts_with, contents):
    return list(filter(lambda x: x.startswith(starts_with), contents.split('\n')))[0][32:]

def get_rows(game_id, contents):
    description = re.search('([\w\-]+)\s+the\s+([\w\-]+[\s\w\-]*)\s+\(([\w\s]+)\)', contents)
    hp, max_hp = get_double('Health:\s+([\-\d]+)/(\d+)', contents)
    mp, max_mp = get_double('Magic:\s+(\d+)/(\d+)', contents)
    spell_levels, max_spell_levels = get_double('Spells:\s+(\d+)/(\d+) levels left', contents)

    out = [
        ('game_id',            game_id),
        ('name',               description.group(1)),
        ('title',              description.group(2)),
        ('species_background', description.group(3)),
        ('turns',              get_value('Turns:\s+(\d+)', contents)),
        ('time',               get_value('Time:\s+([\d\w\:]+)', contents)),
        ('hp',                 hp),
        ('max_hp',             max_hp),
        ('ac',                 get_value('AC:\s+(\d+)', contents)),
        ('str',                get_value('Str:\s+(\d+)', contents)),
        ('xl',                 get_value('XL:\s+(\d+)', contents)),
        ('next_xl',            get_value('Next:\s+(\d+)\%', contents)),
        ('mp',                 mp),
        ('max_mp',             max_mp),
        ('ev',                 get_value('EV:\s+(\d+)', contents)),
        ('int',                get_value('Int:\s+(\d+)', contents)),
        ('god',                get_value('God:\s*([\w]+)\n', contents)),
        ('gold',               get_value('Gold:\s+(\d+)', contents)),
        ('sh',                 get_value('SH:\s+(\d+)', contents)),
        ('dex',                get_value('Dex:\s+(\d+)', contents)),
        ('spell_levels',       spell_levels),
        ('max_spell_levels',   max_spell_levels),
        ('rFire',              get_value('rFire\s+([.x+] [.x+] [.x+])', contents)),
        ('rCold',              get_value('rCold\s+([.x+] [.x+] [.x+])', contents)),
        ('rNeg',               get_value('rNeg\s+([.x+] [.x+] [.x+])', contents)),
        ('rPois',              get_value('rPois\s+([.x+])', contents)),
        ('rElec',              get_value('rElec\s+([.x+])', contents)),
        ('rCorr',              get_value('rCorr\s+([.x+])', contents)),
        ('SeeInvis',           get_value('SeeInvis\s+([.x+])', contents)),
        ('Gourm',              get_value('Gourm\s+([.x+])', contents)),
        ('Faith',              get_value('Faith\s+([.x+])', contents)),
        ('Spirit',             get_value('Spirit\s+([.x+])', contents)),
        ('Reflect',            get_value('Reflect\s+([.x+])', contents)),
        ('Harm',               get_value('Harm\s+([.x+])', contents)),
        ('MR',                 get_value('MR\s+([.+]{5})', contents)),
        ('Stlth',              get_value('Stlth\s+([.+]{10})', contents)),
        ('HPRegen',            get_value('HPRegen\s+(\d+\.\d+)/turn', contents)),
        ('MPRegen',            get_value('MPRegen\s+(\d+\.\d+)/turn', contents)),
        ('weapon',             get_positional('rFire', contents)),
        ('shield',             get_positional('rCold', contents)),
        ('armour',             get_positional('rNeg', contents)),
        ('helmet',             get_positional('rPois', contents)),
        ('cloak',              get_positional('rElec', contents)),
        ('gloves',             get_positional('rCorr', contents)),
        ('boots',              get_positional('MR', contents)),
        ('amulet',             get_positional('Stlth', contents)),
        ('ring_right',         get_positional('HPRegen', contents)),
        ('ring_left',          get_positional('MPRegen', contents)),
        ('status_effects',     get_value('\n@:\s+(.*)\n', contents)),
        ('modifiers',          get_value('\nA:\s+(.*)\n', contents)),
        ('abilities',          get_value('\na:\s+(.*)\n', contents)),
    ]

    return [
        map(lambda x: x[1], out)
    ]

if __name__ == '__main__':
    files = glob.glob('{}/*.txt'.format(os.environ.get('path')))
    for file_name in files:
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(game_id, contents)
        write_rows_to_csv(rows, file_name)
        print(file_name)

