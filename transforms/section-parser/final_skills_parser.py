from common import run_parser
import re


def get_rows(game_id, contents):
    pattern = '\s+([\-\+\*])\s+Level\s+(\d+\.\d)\s+([\s\w]+)'
    rows = []
    for line in contents.split('\n'):
        match = re.search(pattern, line)
        if match is not None:
            rows.append(game_id + [
                match.group(1).strip(),
                match.group(2).strip(),
                match.group(3).strip(),
            ])

    return rows

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

