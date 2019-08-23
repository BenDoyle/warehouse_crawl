from common import build_parser
from common import run_parser
import re

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=build_parser(
            split_on='\n',
            filter_by=lambda line_index, line: line_index > 1,
            map_function=lambda game_id, line: game_id + [line]
        )
    )
