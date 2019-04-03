import re
import os

SECTION_PATTERNS = (
    ('game_version',                 'Dungeon Crawl Stone Soup version 0\.23\.0 \(tiles\) character file\.'),
    ('game_seed',                    'Game seed: \d+'),
    ('prose_summary',                '\d+ [\w\s]+ \(level \d+, [\-0-9]+/\d+ HPs\)'),
    ('final_stats',                  '\w+ the \w+ \([\w\s]+\)\s+Turns: \d+, Time: [0-9:]+'),
    ('final_exploration_summary',    'You were on '),
    ('final_inventory',              'Inventory:'),
    ('final_skills',                 'Skills:'),
    ('final_spells',                 'Your Spells\s+Type\sPower\s+Failure\s+Level\s+Hunger'),
    ('final_library',                'Your spell library contained the following spells:'),
    ('final_dungeon_overview',       'Dungeon Overview and Level Annotations'),
    ('final_altars',                 'Altars:'),
    ('final_shops',                  'Shops:'),
    ('final_annotations',            'Annotations:'),
    ('final_abilities',              'Innate Abilities, Weirdness & Mutations'),
    ('final_messages',               'Message History\n\n\w+'),
    ('final_map',                    '\n\n'),
    ('final_vanquished',             'Vanquished Creatures'),
    ('notes',                        'Notes'),
    ('skill_progression',            'Skill\s+XL:'),
    ('action_totals',                'Action\s+\|'),
)

def section_log_string(contents):
    def find_end(reduced_contents, reduced_section_patterns):
        for section, pattern in reduced_section_patterns:
            match = re.search(pattern, reduced_contents)
            if match:
                return match.span(0)[0]

        return None

    sections = {}
    for section_number, (section, pattern) in enumerate(SECTION_PATTERNS):
        match = re.search(pattern, contents)
        if match:
            end_of_section_match = match.span(0)[1]
            end_position = find_end(contents[end_of_section_match:], SECTION_PATTERNS[section_number+1:])
            if end_position:
                end_position = end_position + end_of_section_match
            sections[section] = contents[0:end_position]
            contents = contents[end_position:]
        else:
            sections[section] = None

    return sections

if __name__ == '__main__':

    # 'data/morgues/morgue-Ysoep-20190225-205833.txt'
    file_name = os.environ.get('filename')
    file_handle = open(file_name, mode='r', errors='ignore')
    contents = file_handle.read()
    file_handle.close()
    sections = section_log_string(contents)

    for section in map(lambda s: s[0], SECTION_PATTERNS):
        try:
            os.makedirs('data/0.23.0/{}'.format(section))
        except:
            pass

        outfile_name = 'data/0.23.0/{}/{}-{}'.format(section, section, os.path.basename(file_name))
        if sections[section]:
            file_handle = open(outfile_name, 'w')
            file_handle.write(sections[section])
            file_handle.close()




