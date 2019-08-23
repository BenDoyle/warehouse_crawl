from common import run_parser
import re


def get_rows(game_id, contents):
    seed_info = re.search('Game seed: (\d+)', contents)
    game_seed = seed_info.group(1).strip()
    return [game_id + [
        game_seed,
    ]]

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

