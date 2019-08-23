from common import run_parser
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
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

