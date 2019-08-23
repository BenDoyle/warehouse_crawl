from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
from notes_common import get_notes
import os
import re
import glob

def get_rows(contents):
    notes = get_notes(game_id, contents)
    killed_re = '^Killed\s+(.*)$'

    output = []
    for line in notes:
        if re.match(killed_re, line[6]) is not None:
            info = re.search(killed_re, line[6])

            description = info.group(1).strip()

            if description.find('ghost') > 0:
                monster_type = 'ghost'
            elif description.find('pandemonium lord') > 0:
                monster_type = 'the pandemonium lord'
            elif description[0].islower():
                monster_type = 'common'
            else:
                monster_type = 'unique'

            if line != notes[-1]:
                output.append(line + [
                    monster_type,
                    description,  # killed
                ])
    return output

if __name__ == '__main__':
    files = glob.glob('{}/*.txt'.format(os.environ.get('input_path')))
    output_path = os.environ.get('output_path')
    for file_name in files:
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(contents)
        write_rows_to_csv(rows, file_name, output_path)
        print(file_name)
