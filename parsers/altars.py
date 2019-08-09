from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
import os
import re
import glob

def get_rows(contents):
    lines = contents.strip().split('\n')
    assert lines[0][0:5] == 'Notes'

    # Found a faded altar of an unknown god.
    altars_re = '^\s*(\d+)\s+\|\s+(\w+):(\d+)\s+\|\s+Found\s+(.*)(altar of)\s+(.*)\.$'

    output = []
    for line in lines[2:]:
        if re.match(altars_re, line) is not None:
            info = re.search(altars_re, line)

            output.append([
                game_id,
                int(info.group(1)),     # turn
                info.group(2).strip(),  # branch_symbol
                int(info.group(3)),     # branch_level
                info.group(4).strip(),  # description
                info.group(6).strip(),  # god
            ])
    return output

if __name__ == '__main__':
    files = glob.glob('{}/*.txt'.format(os.environ.get('path')))
    for file_name in files:
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(contents)
        write_rows_to_csv(rows, file_name, 'altars')
        print(file_name)
