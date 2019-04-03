import re
import os
import csv


def get_game_id(file_name):
    basename = os.path.basename(file_name)
    match = re.match('(.*)-morgue-(.*)-(\d{8})-(\d{6})\.txt', basename)

    return '{}-{}-{}'.format(match.group(2), match.group(3), match.group(4))

if __name__ == '__main__':

    file_name = os.environ.get('filename')
    file_handle = open(file_name, mode='r', errors='ignore')
    contents = file_handle.read()
    file_handle.close()
    game_id = get_game_id(file_name)
    rows = [
        [game_id, altar]
        for altar in contents.strip().split('\n')[1:]
    ]
    if rows:
        outfile_name = file_name[0:-3] + 'csv'
        with open(outfile_name, 'w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(rows)


