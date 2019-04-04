from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
import os
import glob
import re

def get_rows(game_id, contents):
    pattern = '\s+([\-\+\*])\s+Level\s+(\d+\.\d)\s+([\s\w]+)'
    rows = []
    for line in contents.split('\n'):
        match = re.search(pattern, line)
        if match is not None:
            rows.append([
                game_id,
                match.group(1),
                match.group(2),
                match.group(3),
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

