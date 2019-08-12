from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
from notes_common import get_notes
import os
import re
import glob

def get_rows(contents):
    notes = get_notes(game_id, contents)
    unlearn_re = '^Your memory of(.*)unravels\.$'

    output = []
    for line in notes:
        if re.match(unlearn_re, line[4]) is not None:
            info = re.search(unlearn_re, line[4])

            output.append(line + [
                info.group(1).strip(),  # spell_name
            ])
    return output

if __name__ == '__main__':
    files = glob.glob('{}/*.txt'.format(os.environ.get('path')))
    for file_name in files:
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(contents)
        write_rows_to_csv(rows, file_name, 'unlearned')
        print(file_name)
