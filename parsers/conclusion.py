from common import get_game_id
from common import write_rows_to_csv
from common import read_text_file
from notes_common import get_notes
import os
import re
import glob

def get_rows(contents):
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
    files = glob.glob('{}/*.txt'.format(os.environ.get('path')))
    for file_name in files:
        contents = read_text_file(file_name)
        game_id = get_game_id(file_name)
        rows = get_rows(contents)
        write_rows_to_csv(rows, file_name, 'conclusion')
        print(file_name)
