from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    notes = get_notes(game_id, contents)
    skill_re = '^Reached skill level\s+(\d+)\s+in(.*)$'

    output = []
    for line in notes:
        if re.match(skill_re, line[6]) is not None:
            info = re.search(skill_re, line[6])

            output.append(line + [
                int(info.group(1)),     # skill_level
                info.group(2).strip(),  # skill
            ])
    return output

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

