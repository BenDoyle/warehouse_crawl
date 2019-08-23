from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    notes = get_notes(game_id, contents)
    identified_re = '^Identified\s+(.*)$'

    output = []
    for line in notes:
        if re.match(identified_re, line[6]) is not None:
            info = re.search(identified_re, line[6])

            description = info.group(1).strip()

            output.append(line + [
                description,  # killed
            ])
    return output

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

