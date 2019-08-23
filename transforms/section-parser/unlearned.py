from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    notes = get_notes(game_id, contents)
    unlearn_re = '^Your memory of(.*)unravels\.$'

    output = []
    for line in notes:
        if re.match(unlearn_re, line[6]) is not None:
            info = re.search(unlearn_re, line[6])

            output.append(line + [
                info.group(1).strip(),  # spell_name
            ])
    return output

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

