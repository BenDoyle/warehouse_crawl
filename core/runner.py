import argparse
import os
import subprocess
import sys
import re
import tempfile

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

def resolve_manifest_variables(manifest):
    assert manifest.get('data'), "App manifest does not have a 'data' path"
    datapath = manifest['data']
    tmpdir = os.path.join(datapath, 'tmp')
    var_patterns = [
        re.compile(r'\${(\w+)\.(\w+)}'),
        re.compile(r'\$(\w+)\.(\w+)')
    ]
    var_pattern = var_patterns[1]  # temp; fix this to try both patterns

    def variable_value(name_tuple, named_steps):
        if name_tuple == ('tmp', 'dir'):
            return value.replace('$tmp.dir', temp_directory(tmpdir))
        if name_tuple == ('tmp', 'file'):
            return value.replace('$tmp.file', temp_file(tmpdir))
        
        step_name, option = name_tuple
        assert step_name in named_steps, 'Invalid placeholder: ${}; valid names include: {}'.format(
            step_name, sorted(list(named_steps.keys())))
        assert option in named_steps[step_name], 'Invalid placeholder: ${}.{}; valid option names include: {}'.format(
            step_name, option, sorted(list(named_steps[step_name].keys())))
        return named_steps[step_name][option]
    
    for _, steps in manifest['jobs'].items():
        named_steps = {}
        for step in steps:
            for name, value in step.items():
                if not isinstance(value, str):
                    continue
                match = var_pattern.match(value.strip())
                if match:
                    step[name] = variable_value(match.groups(), named_steps)
            if 'name' in step:
                named_steps[step['name']] = step
                    

def run_app(manifest, dryrun=False, transforms_repo_path=None):
    print('Running app: {}'.format(manifest['name']))
    print(' > Discovering transforms...')
    transforms = discover_transforms(transforms_repo_path or TRANSFORMS_REPO_PATH)

    resolve_manifest_variables(manifest)

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
