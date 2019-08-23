from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    notes = get_notes(game_id, contents)
    noticed_re = '^Noticed\s+(.*)$'

    output = []
    for line in notes:
        if re.match(noticed_re, line[6]) is not None:
            info = re.search(noticed_re, line[6])

            description = info.group(1).strip()

            if description.find('ghost') > 0:
                monster_type = 'ghost'
            elif description.find('pandemonium lord') > 0:
                monster_type = 'the pandemonium lord'
            elif description[0].islower():
                monster_type = 'common'
            else:
                monster_type = 'unique'

            output.append(line + [
                monster_type,
                description,  # noticed
            ])
    return output

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

