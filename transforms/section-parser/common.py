import os
import glob
import re
import csv
from datetime import datetime

def get_game_id(file_name):
    basename = os.path.basename(file_name)
    match = re.match('(.*)-morgue-(.*)-(\d{8})-(\d{6})\.txt', basename)

    ts = datetime(
        int(match.group(3)[0:4]),
        int(match.group(3)[4:6]),
        int(match.group(3)[6:8]),
        int(match.group(4)[0:2]),
        int(match.group(4)[2:4]),
        int(match.group(4)[4:6])
    )

    return [match.group(2), int(match.group(3)), ts]


def write_csv(outfile_name, rows):
    with open(outfile_name, 'w') as f:
        # postgresql cannot handle escaped commas
        # writer = csv.writer(f, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_NONE)
        writer = csv.writer(f, delimiter='~', escapechar='\\', quoting=csv.QUOTE_NONE)
        writer.writerows(rows)


def read_text_file(file_name):
    file_handle = open(file_name, mode='r', errors='ignore')
    contents = file_handle.read()
    file_handle.close()

    return contents


def write_rows_to_csv(rows, file_name, output_path):
    if rows:
        tokens = file_name.split('/')
        try:
            os.makedirs(output_path)
        except:
            pass
        outfile_name = '/'.join([output_path, tokens[-1]])
        outfile_name = outfile_name[0:-4] + '.csv'
        write_csv(outfile_name, rows)


def run_parser(input_path_string, output_path_string, get_rows):
    input_path=os.environ.get(input_path_string),
    output_path=os.environ.get(output_path_string),
    files = glob.glob('{}/*.txt'.format(input_path))
    for file_name in files:
        print(file_name)
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(game_id, contents)
        write_rows_to_csv(rows, file_name, output_path)


