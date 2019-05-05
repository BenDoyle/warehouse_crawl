import argparse
import os
import subprocess
import sys
import re
import tempfile
from collections import OrderedDict

import yaml

TRANSFORMS_REPO_PATH = os.path.abspath(os.path.dirname(__file__)+'/../transforms')
REQUIRED_TRANSFORM_FIELDS = {'name', 'run-command'}

def load_yaml(path):
    with open(path, 'r') as fd:
        try:
            manifest = yaml.load(fd, Loader=yaml.FullLoader)
            return manifest if isinstance(manifest, dict) else None
        except yaml.YAMLError:
            return None

def discover_transforms(transforms_repo_path):
    transforms_paths = [path[0] for path in os.walk(transforms_repo_path) if 'manifest.yml' in path[2]]
    transforms = {}
    for path in transforms_paths:
        manifest = load_yaml('{}/manifest.yml'.format(path))
        if not manifest or REQUIRED_TRANSFORM_FIELDS - set(manifest.keys()) :
            continue
        transforms[manifest['name']] = {
            'path': path,
            'manifest': manifest
        }
    return transforms

def execute_job_steps(job_name, steps, transforms, dryrun):
    for step in steps:
        if 'transform' in step:
            execute_transform(step, transforms, dryrun)
        elif 'publish-to' in step:
            execute_publish(step, transforms, dryrun)

def execute_transform(step, transforms, dryrun):
    name = step['transform']
    options = {name: value for (name, value) in step.items() if name != 'transform'}

    assert name in transforms, 'Unknown transform: {}, should be one of: {}'.format(name, set(transforms.keys()))
    path = transforms[name]['path']
    manifest = transforms[name]['manifest']
    
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

def execute_publish(step, transforms, dryrun):
    pass

def temp_directory(root):
    if not os.path.exists(root):
        os.makedirs(root)
    return tempfile.mkdtemp('__', dir=root)

def temp_file(root):
    if not os.path.exists(root):
        os.makedirs(root)
    fd, path = tempfile.mkstemp('__', dir=root)
    os.close(fd)
    return path

def resolve_manifest_placeholders(manifest):
    assert manifest.get('data'), "App manifest does not have a 'data' path"
    datapath = manifest['data']
    tmpdir = os.path.join(datapath, 'tmp')

    def variable_value(name_tuple, named_steps, previous_step):
        if name_tuple == ('tmp', 'dir'):
            return value.replace('$tmp.dir', temp_directory(tmpdir))
        if name_tuple == ('tmp', 'file'):
            return value.replace('$tmp.file', temp_file(tmpdir))
        if name_tuple[0].lower() == 'previous':
            if not previous_step:
                raise Exception('Cannot use $previous placeholder on the first step')
            if name_tuple[1] not in named_steps[previous_step]:
                raise Exception('No previous value found for $previous.{} (previous == "{}")'.format(name_tuple[1], previous_step))
            return named_steps[previous_step][name_tuple[1]]
        
        step_name, option = name_tuple
        assert step_name in named_steps, 'Invalid placeholder: ${}; valid names include: {}'.format(
            step_name, sorted(list(named_steps.keys())))
        assert option in named_steps[step_name], 'Invalid placeholder: ${}.{}; valid option names include: {}'.format(
            step_name, option, sorted(list(named_steps[step_name].keys())))
        return named_steps[step_name][option]

    def resolve_placeholders(value, named_steps, previous_step):
        parens_pattern = re.compile(r'\${(\w+)\.(\w+)}')
        simple_pattern = re.compile(r'\$(\w+)\.(\w+)')
        pos = 0
        value = value.strip()
        while True:
            match = parens_pattern.search(value, pos) or simple_pattern.match(value, pos)
            if match:
                resolved = variable_value(match.groups(), named_steps, previous_step)
                value = value[:match.start()] + resolved + value[match.end():]
                pos = match.start()
            else:
                break
        return value
    
    for _, steps in manifest['jobs'].items():
        named_steps = OrderedDict({})
        for step in steps:
            for name, value in step.items():
                if not isinstance(value, str):
                    continue
                if '$' in value:
                    value = resolve_placeholders(value, named_steps, previous_step=list(named_steps.keys() or [None])[-1])
                    step[name] = value
            if 'name' in step:
                named_steps[step['name']] = step
                    

def run_app(manifest, dryrun=False, transforms_repo_path=None):
    print('Running app: {}'.format(manifest['name']))
    print(' > Discovering transforms...')
    transforms = discover_transforms(transforms_repo_path or TRANSFORMS_REPO_PATH)

    resolve_manifest_placeholders(manifest)

    for (job_name, steps) in manifest['jobs'].items():
        execute_job_steps(job_name, steps, transforms, dryrun)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('App runner')
    parser.add_argument('manifest', help='Path to app manifest YAML file')
    parser.add_argument('--dryrun', action='store_true', help='Print the transform commands instead of executing them')
    args = parser.parse_args()
    
    manifest_path = os.path.abspath(args.manifest)
    if not os.path.exists(manifest_path):
        print('File does not exist: {}'.format(manifest_path))
        exit(code=1)

    manifest = load_yaml(manifest_path)
    run_app(manifest, args.dryrun)
