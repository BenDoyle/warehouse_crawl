import os
import pathlib
import re
from collections import defaultdict
import codecs

version_pattern = re.compile('Dungeon Crawl Stone Soup version ([0-9]+[.][0-9]+)[.-]')

def get_version(path):
    with open(path, encoding='iso-8859-1') as f:
        first_line = f.readline()
    match = version_pattern.search(first_line)
    return match[1] if match else None

def find_morgues(base_path):
    path = pathlib.Path(base_path)
    for file in path.glob('**/morgue-*.txt'):
        yield file.as_posix()

if __name__ == '__main__':
    options = ['morgues', 'output']
    required = ['morgues', 'output']

    env = {
        option: os.environ.get(option.upper())
        for option in options
    }
    missing_options = set(required) & set(option for option, value in env.items() if not value)
    if set(required) & set(option for option, value in env.items() if not value):
        raise Exception('Missing required options: {}'.format(missing_options))

    morgues_path = env['morgues']
    if not os.path.exists(morgues_path):
        raise Exception('Invalid morgues path: {}'.format(morgues_path))

    print('* Classifying morgue files in {}'.format(morgues_path))
    versions = defaultdict(set)
    for i, path in enumerate(find_morgues(morgues_path)):
        version = get_version(path)
        print('  > ({}) {}'.format(i + 1, path))
        if version and version.startswith('0.'):
            versions[version].add(path)

    output_path = env['output']
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    print('* Writing file lists')
    for version in sorted(versions.keys()):
        version_file = os.path.join(output_path, '{version}.txt'.format(version=version))
        print(' > {}'.format(version_file))
        with open(version_file, 'w') as f:
            for path in versions[version]:
                f.write(path + '\n')
