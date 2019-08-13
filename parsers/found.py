from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
from notes_common import get_notes
import os
import re
import glob

def get_rows(contents):
    notes = get_notes(game_id, contents)
    god_re = '^Found\s+(.*)altar of\s+(.*)\.$'
    found_re = '^Found\s+(.*)\.$'

    output = []
    for line in notes:
        if re.match(god_re, line[6]) is None and re.match(found_re, line[6]) is not None:
            info = re.search(found_re, line[6])

            output.append(line + [
                info.group(1).strip(),  # found
            ])
    return output

if __name__ == '__main__':
    files = glob.glob('{}/*.txt'.format(os.environ.get('path')))
    for file_name in files:
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(contents)
        write_rows_to_csv(rows, file_name, 'found')
        print(file_name)
