from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
import os
import glob
import re

def get_rows(game_id, contents):
    version_info = re.search('(\d+)\.(\d+)(\.([\d]+))?(\-([\w\d\-]+))*\s\((\w+)\)', contents)
    version_string = version_info.group(0).strip()
    major_version = version_info.group(1).strip()
    minor_version = version_info.group(2).strip()
    patch_level = version_info.group(4)
    build = version_info.group(6)
    view = version_info.group(7)

    return [game_id + [
        version_string,
        major_version,
        minor_version,
        patch_level,
        build,
        view,
    ]]

if __name__ == '__main__':
    files = glob.glob('{}/*.txt'.format(os.environ.get('path')))
    for file_name in files:
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(game_id, contents)
        write_rows_to_csv(rows, file_name)
        print(file_name)

