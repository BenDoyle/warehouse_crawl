import argparse
import os
import subprocess
import sys
import re
import tempfile

import yaml

PROCESSORS_REPO_PATH = os.path.abspath(os.path.dirname(__file__)+'/../processors')
REQUIRED_PROCESSOR_FIELDS = {'name', 'run-command'}
REQUIRED_JOB_FIELDS = {'processor'}

def load_yaml(path):
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
        manifest = load_yaml('{}/manifest.yml'.format(path))
        if not manifest or REQUIRED_PROCESSOR_FIELDS - set(manifest.keys()) :
            continue
        processors[manifest['name']] = {
            'path': path,
            'manifest': manifest
        }
    return processors

def execute_processors(steps, processors, dryrun):
    for step in steps:
        execute_processor(step, processors, dryrun)

def execute_processor(step, processors, dryrun):
    name = step['processor']
    options = {name: value for (name, value) in step.items() if name != 'processor'}

    assert name in processors, 'Unknown processor: {}, should be one of: {}'.format(name, set(processors.keys()))
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

def temp_directory(root):
    return tempfile.mkdtemp('__', dir=root)

def temp_file(root):
    return tempfile.mkstemp('__', dir=root)

def validate_app_manifest(manifest):
    assert manifest.get('data'), "App manifest does not have a 'data' path"
    datapath = manifest['data']
    tmpdir = os.path.join(datapath, 'tmp')
    var_pattern = re.compile(r'\$(\w+)\.(\w+)')

    def variable_value(name_tuple, named_steps):
        if name_tuple == ('tmp', 'dir'):
            return value.replace('$tmp.dir', temp_directory(tmpdir))
        if name_tuple == ('tmp', 'file'):
            return value.replace('$tmp.file', temp_file(tmpdir))
        
        step_name, option = name_tuple
        assert step_name in named_steps, 'Invalid placeholder: ${}; valid names include: {}'.format(
            step_name, list(sorted(named_steps.keys())))
        assert option in named_steps[step_name], 'Invalid placeholder: ${}.{}; valid option names include: {}'.format(
            step_name, option, list(sorted(named_steps[step_name].keys())))
        return named_steps[step_name][option]
    
    for index, job in enumerate(manifest['jobs']):
        manifest['jobs'][index] = steps = [job] if isinstance(job, dict) else job
        # named_steps = {step['name']: step for step in steps.items() if 'name' in step}
        named_steps = {}
        for step in steps:
            for name, value in step.items():
                if not isinstance(value, str):
                    continue
                match = var_pattern.match(value.strip())
                if match:
                    step[name] = variable_value(match.groups(), named_steps)
            if step.get('name'):
                named_steps[step['name']] = step
                    

def run_app(manifest, dryrun=False, processors_repo_path=None):
    print('Running app: {}'.format(manifest['name']))
    print(' > Discovering processors...')
    processors = discover_processors(processors_repo_path or PROCESSORS_REPO_PATH)

    validate_app_manifest(manifest)

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

    manifest = load_yaml(manifest_path)
    run_app(manifest, args.dryrun)
