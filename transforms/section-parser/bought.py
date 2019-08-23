from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    notes = get_notes(game_id, contents)
    bought_re = '^Bought\s+(.*)\s+for\s+(\d+)\s+gold pieces$'

    output = []
    for line in notes:
        if re.match(bought_re, line[6]) is not None:
            info = re.search(bought_re, line[6])

            output.append(line + [
                info.group(1).strip(),  # bought
                int(info.group(2))      # price
            ])
    return output

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

