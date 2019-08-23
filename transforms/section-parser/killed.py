from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    notes = get_notes(game_id, contents)
    killed_re = '^Killed\s+(.*)$'

    output = []
    for line in notes:
        if re.match(killed_re, line[6]) is not None:
            info = re.search(killed_re, line[6])

            description = info.group(1).strip()

            if description.find('ghost') > 0:
                monster_type = 'ghost'
            elif description.find('pandemonium lord') > 0:
                monster_type = 'the pandemonium lord'
            elif description[0].islower():
                monster_type = 'common'
            else:
                monster_type = 'unique'

            if line != notes[-1]:
                output.append(line + [
                    monster_type,
                    description,  # killed
                ])
    return output

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

