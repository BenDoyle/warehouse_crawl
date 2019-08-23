import glob
import os
import subprocess
import sys

def run(input_path, output_file):
    files = glob.glob('{}/*.csv'.format(input_path))
    output_path = '/'.join(output_file.split('/')[0:-1])
    try:
        os.makedirs(output_path)
    except:
        pass

    command = "rm {}".format(output_file)
    subprocess.run(command.split(' '), stdout=sys.stdout, stderr=sys.stderr)
    command = "touch {}".format(output_file)
    subprocess.run(command.split(' '), stdout=sys.stdout, stderr=sys.stderr)

    with open(output_file, 'w') as out:
        for file_name in files:
            print(file_name)
            command = "cat {}".format(file_name)
            # import pdb; pdb.set_trace()
            subprocess.run(command.split(' '), stdout=out, stderr=sys.stderr)

if __name__ == '__main__':
    required = ['input_path', 'output_file']
    options = required
    env = {
        option: os.environ.get(option.upper())
        for option in options
    }
    missing_options = set(required) & set(option for option, value in env.items() if not value)
    if set(required) & set(option for option, value in env.items() if not value):
        raise Exception('Missing required options: {}'.format(missing_options))

    run(**env)
