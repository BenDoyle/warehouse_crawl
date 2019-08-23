from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    notes = get_notes(game_id, contents)
    mutation_re = '^(Gained|Lost) mutation:\s*\[?(.*)\]?\[(.*)\]\s*$'

    output = []
    for line in notes:
        if re.match(mutation_re, line[6]) is not None:
            info = re.search(mutation_re, line[6])

            output.append(line + [
                info.group(1).strip(),                  # status
                info.group(2).strip().replace(']',''),  # mutation
                info.group(3).strip(),                  # source
            ])
    return output

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

