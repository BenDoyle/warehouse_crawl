from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    notes = get_notes(game_id, contents)
    win_re = '^Escaped with the Orb!$'

    output = []
    for line in notes:
        if re.match(win_re, line[6]) is not None:
            output.append(line)
    return output

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

