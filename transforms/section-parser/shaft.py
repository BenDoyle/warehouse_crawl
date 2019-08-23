from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    notes = get_notes(game_id, contents)
    shaft_re = '^You fall through a shaft( for (\d+) floors)?!$'

    output = []
    for line in notes:
        if re.match(shaft_re, line[6]) is not None:
            info = re.search(shaft_re, line[6])

            if info.group(1):
                floors = int(info.group(2))
            else:
                floors = 1

            output.append(line + [
                floors
            ])
    return output

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

