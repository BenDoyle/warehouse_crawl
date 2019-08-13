from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
from notes_common import get_notes
import os
import re
import glob

def get_rows(contents):
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
    files = glob.glob('{}/*.txt'.format(os.environ.get('path')))
    for file_name in files:
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(contents)
        write_rows_to_csv(rows, file_name, 'upgrades')
        print(file_name)
