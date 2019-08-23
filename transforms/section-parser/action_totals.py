from common import run_parser
import re


def get_rows(game_id, contents):
    lines = contents.strip().split('\n')
    assert lines[0][0:6] == 'Action'

    output = []
    action_category = None
    for line in lines[2:]:

        head, total = line.split('||')
        total = int(total.strip())
        items = head.split('|')
        description = items[0]
        description_elements = description.split(':')

        if len(description_elements) == 2:
            action_category = description_elements[0].strip()
            action = description_elements[1].strip()
        else:
            action = description_elements[0].strip()

        counts = items[1:]
        if len(counts) == 0:
            counts = [total]
        else:
            counts = [int(i.strip()) if len(i.strip()) > 0 else None for i in counts]
        counts = counts + [None for i in range(len(counts), 9)]

        for index, count in enumerate(counts):
            output.append(game_id + [
                action_category,
                action,
                'Level {} - Level {}'.format(3 * index + 1, 3 * (index + 1)),
                count
            ])

    return output


if __name__ == '__main__':
    run_parser(
        input_path_string='input_path',
        output_path_string='output_path',
        get_rows=get_rows,
    )
