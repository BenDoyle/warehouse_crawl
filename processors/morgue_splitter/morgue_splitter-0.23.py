import glob
import re
import os

SECTION_PATTERNS = {
    'game_version':                 'Dungeon Crawl Stone Soup version 0\.23(\.\d+)?[\-\w\d]* \(\w+\) character file\.',
    'game_seed':                    'Game seed: \d+',
    'prose_summary':                '\d+ [\-\w\s]+ \(level \d+, [\-0-9]+/\d+',
    'final_stats':                  '[\-\w]+\s+the\s+[\s\-\w]+\s\([\w\s]+\)\s+Turns:\s+\d+,\s+Time:\s+[0-9:]+',
    'final_exploration_summary':    'You were [oi]n|You escaped',
    'final_inventory':              'Inventory:',
    'final_skills':                 'Skills:',
    'final_spells':                 'You had [\d\w]+ spell level(s)? left.|You couldn\'t memorise any spells.',
    'final_library':                'Your spell library contained the following spells:|Your spell library was empty.',
    'final_dungeon_overview':       'Dungeon Overview and Level Annotations',
    'final_altars':                 'Altars:',
    'final_shops':                  'Shops:',
    'final_annotations':            'Annotations:',
    'final_abilities':              'Innate Abilities, Weirdness & Mutations',
    'final_messages':               'Message History\n\n',
    'final_vanquished':             'Vanquished Creatures\n',
    'final_map':                    '\n\n(.+\n)+\n\n(You could see|There were no monsters in sight!)',
    'final_portals':                'Portals',
    'notes':                        'Notes',
    'skill_progression':            'Skill\s+XL:',
    'action_totals':                'Action\s+\|',
    'levels_and_vaults_discovered': 'Levels and vault maps discovered:',
}

OPTIONAL_SECTIONS = [
    'final_altars',                 # some logs do not print an altars list, even if found. e.g. morgue-stickyfingers-20190213-154231.txt
    'final_abilities',              # games without mutations
    'final_shops',                  # shops are not discovered in this game
    'final_annotations',            # annotatable things are not present in this game
    'final_vanquished',             # games with no vanquished creatures
    'skill_progression',            # games that end before level 2 is reached
    'action_totals',                # games without a single action
    'final_portals',                # not all games have portals
    'levels_and_vaults_discovered', # not all games have this
]

def section_log_string(contents):

    def min_or_none(breakpoints, start):
        larger = set(filter(lambda x: x >= start, breakpoints))
        if larger:
            return min(larger)
        else:
            return None

    section_matches = {
        section: list(re.finditer(pattern, contents))
        for section, pattern in SECTION_PATTERNS.items()
    }

    breakpoints = {
        match.span(0)[0]
        for section, matches in section_matches.items()
        for match in matches
    } - {None}

    section_spans = {
        section: matches[0].span(0) if len(matches) > 0 else None
        for section, matches in section_matches.items()
    }

    sections = {
        section: contents[span[0]:min_or_none(breakpoints, span[1])] if span else None
        for section, span in section_spans.items()
    }

    return sections

if __name__ == '__main__':

    files = glob.glob('{}/*.txt'.format(os.environ.get('MORGUES')))
    output_dir = os.path.abspath(os.environ.get('OUTPUT'))

    for file_name in files:
        print(file_name)
        file_handle = open(file_name, mode='r', errors='ignore')
        contents = file_handle.read()
        file_handle.close()
        sections = section_log_string(contents)

        for section in SECTION_PATTERNS.keys():
            try:
                os.makedirs('{}/0.23/{}'.format(output_dir, section))
            except:
                pass

            outfile_name = '{}/0.23/{}/{}-{}'.format(output_dir, section, section, os.path.basename(file_name))

            if sections[section]:
                file_handle = open(outfile_name, 'w')
                file_handle.write(sections[section])
                file_handle.close()
            elif section not in OPTIONAL_SECTIONS:
                print("  missing {}".format(section))
