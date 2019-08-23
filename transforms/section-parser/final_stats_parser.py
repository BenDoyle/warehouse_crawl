from common import run_parser
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
        return (match.group(1).strip(), match.group(2).strip())
    else:
        return (None, None)

def get_positional(starts_with, contents):
    return list(filter(lambda x: x.startswith(starts_with), contents.split('\n')))[0][32:]

def get_rows(game_id, contents):
    description = re.search('([\w\-]+)\s+the\s+([\w\-]+[\s\w\-]*)\s+\(([\w\s]+)\)', contents)
    hp, max_hp = get_double('Health:\s+([\-\d]+)/(\d+)', contents)
    mp, max_mp = get_double('Magic:\s+(\d+)/(\d+)', contents)
    spell_levels, max_spell_levels = get_double('Spells:\s+(\d+)/(\d+) levels left', contents)

    out = game_id + [
        description.group(1).strip(),                       # name
        description.group(2).strip(),                       # title
        description.group(3).strip(),                       # species_background
        get_value('Turns:\s+(\d+)', contents),              # turns
        get_value('Time:\s+([\d\w\:]+)', contents),         # time
        hp,                                                 # hp
        max_hp,                                             # max_hp
        get_value('AC:\s+(\d+)', contents),                 # ac
        get_value('Str:\s+(\d+)', contents),                # str
        get_value('XL:\s+(\d+)', contents),                 # xl
        get_value('Next:\s+(\d+)\%', contents),             # next_xl
        mp,                                                 # mp
        max_mp,                                             # max_mp
        get_value('EV:\s+(\d+)', contents),                 # ev
        get_value('Int:\s+(\d+)', contents),                # int
        get_value('God:\s*([\w]+)(\s*[\[\]\s\.x+*]+)?\s*\n', contents),            # god
        get_value('Gold:\s+(\d+)', contents),               # gold
        get_value('SH:\s+(\d+)', contents),                 # sh
        get_value('Dex:\s+(\d+)', contents),                # dex
        spell_levels,                                       # spell_levels
        max_spell_levels,                                   # max_spell_levels
        get_value('rFire\s+([\.x+] [\.x+] [\.x+])', contents), # rFire
        get_value('rCold\s+([\.x+] [\.x+] [\.x+])', contents), # rCold
        get_value('rNeg\s+([\.x+] [\.x+] [\.x+])', contents),  # rNeg
        get_value('rPois\s+([\.x+])', contents),             # rPois
        get_value('rElec\s+([\.x+])', contents),             # rElec
        get_value('rCorr\s+([\.x+])', contents),             # rCorr
        get_value('SeeInvis\s+([\.x+])', contents),          # SeeInvis
        get_value('Gourm\s+([\.x+])', contents),             # Gourm
        get_value('Faith\s+([\.x+])', contents),             # Faith
        get_value('Spirit\s+([\.x+])', contents),            # Spirit
        get_value('Reflect\s+([\.x+])', contents),           # Reflect
        get_value('Harm\s+([\.x+])', contents),              # Harm
        get_value('MR\s+([.+]{5})', contents),              # MR
        get_value('Stlth\s+([.+]{10})', contents),          # Stlth
        get_value('HPRegen\s+(\d+\.\d+)/turn', contents),   # HPRegen
        get_value('MPRegen\s+(\d+\.\d+)/turn', contents),   # MPRegen
        get_positional('rFire', contents),                  # weapon
        get_positional('rCold', contents),                  # shield
        get_positional('rNeg', contents),                   # armour
        get_positional('rPois', contents),                  # helmet
        get_positional('rElec', contents),                  # cloak
        get_positional('rCorr', contents),                  # gloves
        get_positional('MR', contents),                     # boots
        get_positional('Stlth', contents),                  # amulet
        get_positional('HPRegen', contents),                # ring_right
        get_positional('MPRegen', contents),                # ring_left
        get_value('\n@:\s+(.*)\n', contents),               # status_effects
        get_value('\nA:\s+(.*)\n', contents),               # modifiers
        get_value('\na:\s+(.*)\n', contents),               # abilities
    ]

    return [out]

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )


