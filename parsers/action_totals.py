from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
import os
import glob

CREATE_TABLE = '''
    DROP TABLE IF EXISTS action_totals;
    CREATE TABLE action_totals (
        game_id         VARCHAR(255),
        action_category VARCHAR(255),
        action          VARCHAR(255),
        level_group     VARCHAR(255),
        count           INTEGER
    );
'''

def get_rows(contents):
    lines = contents.strip().split('\n')
    assert lines[0][0:6] == 'Action'

    output = []
    action_category = None
    for line in lines[2:]:

        head, total = line.split('||')
        total = int(total.strip())
        items = head.split('|')
        description = items[0]
        description_elements = description.split(':')

        if len(description_elements) == 2:
            action_category = description_elements[0].strip()
            action = description_elements[1].strip()
        else:
            action = description_elements[0].strip()

        counts = items[1:]
        if len(counts) == 0:
            counts = [total]
        else:
            counts = [int(i.strip()) if len(i.strip()) > 0 else None for i in counts]
        counts = counts + [None for i in range(len(counts), 9)]

        for index, count in enumerate(counts):
            output.append(game_id + [
                action_category,
                action,
                'Level {} - Level {}'.format(3 * index + 1, 3 * (index + 1)),
                count
            ])

    return output


if __name__ == '__main__':
    files = glob.glob('{}/*.txt'.format(os.environ.get('path')))
    for file_name in files:
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(contents)
        write_rows_to_csv(rows, file_name)
        print(file_name)

