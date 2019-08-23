from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    notes = get_notes(game_id, contents)
    upgrade_re = '^.*(\d+)\.(\d+)\.(\d+)-(\d+)-(\w+)\s*$'

    output = []
    for line in notes:
        if re.match(upgrade_re, line[6]) is not None:
            info = re.search(upgrade_re, line[6])

            output.append(line + [
                int(info.group(1)),     # major
                int(info.group(2)),     # minor
                int(info.group(3)),     # patch
                int(info.group(4)),     # build
                info.group(5).strip(),  # build
            ])
    return output

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

