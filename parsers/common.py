import os
import re
import csv

def get_game_id(file_name):
    basename = os.path.basename(file_name)
    match = re.match('(.*)-morgue-(.*)-(\d{8})-(\d{6})\.txt', basename)

    return '{}-{}-{}'.format(match.group(2), match.group(3), match.group(4))


def write_csv(outfile_name, rows):
    with open(outfile_name, 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_NONE)
        writer.writerows(rows)


def read_text_file(file_name):
    file_handle = open(file_name, mode='r', errors='ignore')
    contents = file_handle.read()
    file_handle.close()

    return contents


def write_rows_to_csv(rows, file_name, subfolder=None):
    if rows:
        if subfolder:
            tokens = file_name.split('/')
            tokens.insert(-1, subfolder)
            adjusted_file_name = '/'.join(tokens)
            try:
                os.makedirs('/'.join(tokens[0:-1]))
            except:
                pass
        else:
            adjusted_file_name = file_name

        outfile_name = adjusted_file_name[0:-4] + '.csv'
        write_csv(outfile_name, rows)

