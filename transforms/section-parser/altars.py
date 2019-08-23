from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    notes = get_notes(game_id, contents)
    god_re = '^Found\s+(.*)altar of\s+(.*)\.$'

    output = []
    for line in notes:
        if re.match(god_re, line[6]) is not None:
            info = re.search(god_re, line[6])

            output.append(line + [
                info.group(1).strip(),  # description
                info.group(2).strip(),  # god
            ])
    return output

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

