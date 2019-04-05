import argparse
import os
import subprocess
import sys

import yaml

PROCESSORS_REPO_PATH = os.path.abspath(os.path.dirname(__file__)+'/../processors')
REQUIRED_PROCESSOR_FIELDS = {'name', 'run-command'}
REQUIRED_JOB_FIELDS = {'processor'}

def load_yaml_manifest(path):
    with open(path, 'r') as fd:
        try:
            manifest = yaml.load(fd, Loader=yaml.FullLoader)
            return manifest if isinstance(manifest, dict) else None
        except yaml.YAMLError:
            return None

def discover_processors(processors_repo_path):
    processors_paths = [path[0] for path in os.walk(processors_repo_path) if 'manifest.yml' in path[2]]
    processors = {}
    for path in processors_paths:
        manifest = load_yaml_manifest('{}/manifest.yml'.format(path))
        if not manifest or REQUIRED_PROCESSOR_FIELDS - set(manifest.keys()) :
            continue
        processors[manifest['name']] = {
            'path': path,
            'manifest': manifest
        }
    return processors

def execute_processors(steps, processors, dryrun):
    # TODO: support chaining inputs and outputs with $previous
    for step in steps:
        execute_processor(step, processors, dryrun)

def execute_processor(step, processors, dryrun):
    name = step['processor']
    options = {name: value for (name, value) in step.items() if name != 'processor'}

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

def run_app(manifest, dryrun=False, processors_repo_path=None):
    print('Running app: {}'.format(manifest['name']))
    print(' > Discovering processors...')
    processors = discover_processors(processors_repo_path or PROCESSORS_REPO_PATH)

    for (job_num, job) in enumerate(manifest['jobs']):
        steps = [job] if isinstance(job, dict) else job
        execute_processors(steps, processors, dryrun)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('App runner')
    parser.add_argument('manifest', help='Path to app manifest YAML file')
    parser.add_argument('--dryrun', action='store_true', help='Print the processor commands instead of executing them')
    args = parser.parse_args()
    
    manifest_path = os.path.abspath(args.manifest)
    if not os.path.exists(manifest_path):
        print('File does not exist: {}'.format(manifest_path))
        exit(code=1)

    manifest = load_yaml_manifest(manifest_path)
    run_app(manifest, args.dryrun)
