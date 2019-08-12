import re

def get_notes(game_id, contents):
    assert contents[0:5] == 'Notes'

    note_re = '^\s*(\d+)\s+\|\s+(\w+):([\$\d]+)\s+\|\s+(.*)\s*$'
    multiline_re = '^\s+\|(.*)$'

    lines = contents.strip().split('\n')
    current_line = None
    output = []

    for line in lines[2:]:
        if re.match(note_re, line) is not None:
            if current_line is not None:
                current_line.append(current_note)
                output.append(current_line)

            info = re.search(note_re, line)
            current_line = [
                game_id,
                int(info.group(1)),     # turn
                info.group(2).strip(),  # branch_symbol
                info.group(3).strip(),  # branch_level (could be $)
            ]
            current_note = info.group(4).strip()  # note
        elif re.match(multiline_re, line) is not None:
            info = re.search(multiline_re, line)
            current_note = current_note + info.group(1)

    current_line.append(current_note)
    output.append(current_line)

    return output
