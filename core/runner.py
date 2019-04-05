import os
import sys
import subprocess
import argparse
import yaml

PROCESSORS_REPO_PATH = os.path.abspath(os.path.dirname(__file__)+'/../processors')

def discover_processors(processors_repo_path):
    def load_processor_manifest(path):
        with open(path, 'r') as fd:
            try:
                return yaml.load(fd, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                print(exc)

    processors_repo = os.path.abspath(os.path.dirname(__file__)+'/../processors')
    processors_paths = [path[0] for path in os.walk(processors_repo) if 'manifest.yml' in path[2]]
    processors = {}
    for path in processors_paths:
        manifest = load_processor_manifest('{}/manifest.yml'.format(path))
        processors[manifest['name']] = {
            'path': path,
            'manifest': manifest
        }
    return processors

def execute_step(name, options, processors, dryrun):
    assert name in processors, 'Unknown processor: {}'.format(name)
    path = processors[name]['path']
    manifest = processors[name]['manifest']
    
    command = '{options} {command}'.format(
        options = ' '.join('{}={}'.format(option.upper(), value) for (option, value) in options.items()),
        command = manifest['run-command']
    )
    
    options = {option.upper(): str(value) for (option, value) in options.items()}
    command = manifest['run-command']
    if dryrun:
        print('DRYRUN: Would execute the following command:')
        print('  {options} cd {path} && {cmd}'.format(
            options=' '.join('{}={}'.format(name, value) for (name, value) in options.items()),
            path=path,
            cmd=command
        ))
    else:
        env = dict(os.environ)
        env.update(options)
        command = command.split(' ')
        subprocess.run(command, cwd=path, env=env, stdout=sys.stdout, stderr=sys.stderr)

def load_app_manifest(manifest_path):
    if not os.path.exists(manifest_path):
        print('File does not exist: {}'.format(manifest_path))
        exit(code=1)
    with open(manifest_path, 'r') as fd:
        try:
            return yaml.load(fd, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

def run_app(manifest):
    print('Running app: {}'.format(manifest['name']))
    print(' > Discovering processors...')
    processors = discover_processors(PROCESSORS_REPO_PATH)

    total_steps = len(manifest['steps'])
    for (i, (name, options)) in enumerate(manifest['steps'].items()):
        print('Executing processor {name} [{current}/{total}]'.format(
            name=name, current=i+1, total=total_steps
        ))
        execute_step(name, options, processors, args.dryrun)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('App runner')
    parser.add_argument('manifest', help='Path to app manifest YAML file')
    parser.add_argument('--dryrun', action='store_true', help='Print the processor commands instead of executing them')
    args = parser.parse_args()
    
    manifest_path = os.path.abspath(args.manifest)
    manifest = load_app_manifest(manifest_path)
    run_app(manifest)
    