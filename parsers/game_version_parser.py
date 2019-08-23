from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
import os
import glob
import re

def get_rows(game_id, contents):
    info = re.search('(\d+)\.(\d+)\.(\d+)?(-(\d+))??(-(\w+))?\s\((console|tiles)\)', contents)
    if info:
        return [game_id + [
            info.group(0).strip(),  # string
            int(info.group(1)),     # major
            int(info.group(2)),     # minor
            int(info.group(3)),     # patch
            int(info.group(5))    if info.group(4) else None,     # build
            info.group(7).strip() if info.group(5) else None,  # build
            info.group(8).strip(),  # view
            False,                  # malformed
        ]]
    else:
        info = re.search('(\d+)\.(\d+).*\((console|tiles|webtiles)\)', contents)
        return [game_id + [
            info.group(0).strip(),  # string
            int(info.group(1)),     # major
            int(info.group(2)),     # minor
            None,                   # patch
            None,                   # build
            None,                   # build
            info.group(3).strip(),  # view
            True,                  # malformed
        ]]

if __name__ == '__main__':
    files = glob.glob('{}/*.txt'.format(os.environ.get('input_path')))
    output_path = os.environ.get('output_path')
    for file_name in files:
        print(file_name)
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(game_id, contents)
        write_rows_to_csv(rows, file_name, output_path)

