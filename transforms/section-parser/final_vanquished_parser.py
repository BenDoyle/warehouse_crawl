from common import run_parser
import re


def get_rows(game_id, contents):
    pattern = '^\s+(\d+)?\s+([\s\w]+)(\(([\w\:\d]+)\))?'
    rows = []
    vanquished_by = 'player'
    for line in contents.split('\n'):
        if line == 'Vanquished Creatures (others)':
            vanquished_by = 'others'
        match = re.search(pattern, line)
        if match is not None:
            rows.append(game_id + [
                vanquished_by,
                match.group(1).strip() if match.group(1) else None,
                match.group(2).strip() if match.group(2) else None,
                match.group(3).strip() if match.group(3) else None,
            ])

    return rows

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )


