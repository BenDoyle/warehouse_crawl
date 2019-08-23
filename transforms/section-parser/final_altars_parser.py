from common import run_parser
import re


def get_rows(game_id, contents):
    lines = contents.strip().split('\n')
    assert lines[0] == 'Altars:'
    return [
        game_id + [altar]
        for altar in lines[1:]
    ]

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )


