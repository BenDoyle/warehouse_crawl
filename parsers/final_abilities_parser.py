from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
import os
import glob

def get_rows(contents):
    lines = contents.strip().split('\n')
    assert lines[0] == 'Innate Abilities, Weirdness & Mutations'
    return [
        [game_id, ability]
        for ability in lines[2:]
    ]

if __name__ == '__main__':
    files = glob.glob('{}/*.txt'.format(os.environ.get('path')))
    for file_name in files:
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(contents)
        write_rows_to_csv(rows, file_name)
        print(file_name)

