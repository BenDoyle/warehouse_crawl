from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
import os
import glob
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
    files = glob.glob('{}/*.txt'.format(os.environ.get('path')))
    for file_name in files:
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(game_id, contents)
        write_rows_to_csv(rows, file_name)
        print(file_name)

