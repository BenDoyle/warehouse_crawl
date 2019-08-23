from common import run_parser
from notes_common import get_notes
import re


def get_rows(game_id, contents):
    final_row = get_notes(game_id, contents)[-1]
    acid = re.search('Splashed by(.+)\'s acid', final_row[6])
    impaled = re.search('Impaled on(.+)\'s spines', final_row[6])
    killed = re.search('(.+)by(.+)', final_row[6])
    succumbed = re.search('Succumbed to (.+) poison', final_row[6])

    # status, how, who

    if final_row[6] == 'Starved to death':
        conclusion = ['died', 'starved', 'player']
    elif final_row[6] == 'Quit the game':
        conclusion = ['quit', 'quit', 'player']
    elif final_row[6] == 'Escaped with the Orb!':
        conclusion = ['won', 'won', 'player']
    elif final_row[6] == 'Got out of the dungeon alive.':
        conclusion = ['quit', 'left', 'player']
    elif impaled:
        conclusion = ['died', 'impaled', impaled.group(1).strip()]
    elif acid:
        conclusion = ['died', 'acid', acid.group(1).strip()]
    elif killed:
        conclusion = ['died', killed.group(1).strip(), killed.group(2).strip()]
    elif succumbed:
        conclusion = ['died', 'poison', succumbed.group(1).strip()]
    else:
        conclusion = [None, None, None]

    return [final_row + conclusion]

if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )

