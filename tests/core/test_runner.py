import os
import pytest
import mock
from distutils.dir_util import copy_tree
import re
import yaml

from core import runner

def parse_yaml(yaml_str):
    return yaml.load(yaml_str, yaml.FullLoader)

@pytest.fixture
def processors_fixtures_path():
    return os.path.abspath(os.path.dirname(__file__)+'/../../tests/fixtures/processors')

class TestProcessorDiscovery(object):
    def test_discover_processors(self, processors_fixtures_path):
        processors = runner.discover_processors(processors_fixtures_path)

        names_and_paths = [
            (name, processor['path'])
            for name, processor in processors.items()
        ]
        assert sorted(names_and_paths) == sorted([
            ('morgue-splitter', '{repo_dir}/splitter'.format(repo_dir=processors_fixtures_path)),
            ('morgues-download', '{repo_dir}/download'.format(repo_dir=processors_fixtures_path)),
            ('parser', '{repo_dir}/parser'.format(repo_dir=processors_fixtures_path))
        ])

    def test_discover_processors_ignore_dirs_without_manifests(self, processors_fixtures_path, tmpdir):
        repo_dir = str(tmpdir.mkdir('processors'))
        copy_tree(processors_fixtures_path, repo_dir)
        
        os.mkdir(os.path.join(repo_dir, 'not-a-processor'))
        with open(os.path.join(repo_dir, 'not-a-processor', 'manifest'), 'w') as fd:
            fd.write('not really a manifest')

        processors = runner.discover_processors(repo_dir)

        assert sorted(processors.keys()) == sorted([
            'morgue-splitter', 'morgues-download', 'parser'
        ])

    def test_discover_processors_ignore_invalid_yaml_manifest(self, processors_fixtures_path, tmpdir):
        repo_dir = str(tmpdir.mkdir('processors'))
        copy_tree(processors_fixtures_path, repo_dir)
        
        os.mkdir(os.path.join(repo_dir, 'invalid-yaml-processor'))
        with open(os.path.join(repo_dir, 'invalid-yaml-processor', 'manifest.yml'), 'w') as fd:
            fd.write('not really a manifest')

        processors = runner.discover_processors(repo_dir)

        assert sorted(processors.keys()) == sorted([
            'morgue-splitter', 'morgues-download', 'parser'
        ])

    @pytest.mark.parametrize('required_key', [
        'name', 'run-command'
    ])
    def test_discover_processors_ignore_missing_required_manifest_field(self, required_key, processors_fixtures_path, tmpdir):
        repo_dir = str(tmpdir.mkdir('processors'))
        copy_tree(processors_fixtures_path, repo_dir)
        
        yaml = re.sub(r'^([ \t]*{}\:)'.format('name'), r'# \1', """
name: invalid-manifest-processor
run-command: python run.py
        """, flags=re.MULTILINE)
        os.mkdir(os.path.join(repo_dir, 'invalid-processor'))
        with open(os.path.join(repo_dir, 'invalid-processor', 'manifest.yml'), 'w') as fd:
            fd.write(yaml)

        processors = runner.discover_processors(repo_dir)

        assert sorted(processors.keys()) == sorted([
            'morgue-splitter', 'morgues-download', 'parser'
        ])

@mock.patch('subprocess.run', mock.Mock())
class TestAppManifest(object):
    # @pytest.fixture
    # def write_yaml(self, tmpdir):
    #     def writer(yaml, name=None):
    #         name = name or 'my_app'
    #         path = os.path.join(str(tmpdir.mkdir('apps')), '{}.yml'.format(name))
    #         with open(path, 'w') as fd:
    #             fd.write(yaml)
    #         return path
    #     return writer

    @pytest.fixture
    def app_manifest_simple(self):
        return """
name: Simple app manifest
jobs:
- processor: download
  base_url: http://example.com/data
  throttle: 1000
  output: /tmp/data/morgues
        """

    @pytest.fixture
    def app_manifest_multiple_jobs(self):
        return """
name: Multiple job manifest
jobs:
- processor: download
  base_url: http://example.com/data
  throttle: 1000
  output: /tmp/data/morgues
- processor: splitter
  morgues: /tmp/data/morgues
  output: /tmp/data/splits
        """

    @pytest.fixture
    def app_manifest_composed_job(self):
        return """
name: Single composed job manifest
jobs:
- 
  - processor: download
    base_url: http://example.com/data
    throttle: 1000
    output: /tmp/data/morgues
  - processor: splitter
    morgues: /tmp/data/morgues
    output: /tmp/data/splits
        """

    @mock.patch('core.runner.execute_processor')
    def test_run_app_simple_job(self, execute_processor, app_manifest_simple, processors_fixtures_path):
        manifest = parse_yaml(app_manifest_simple)
        runner.run_app(manifest, processors_repo_path=processors_fixtures_path)

        assert execute_processor.call_count == 1, '`execute_processor` was called an unexpected number of times'
        actual_steps = [call[1].get('step') or call[0][0] for call in execute_processor.call_args_list]
        actual_processors = [call[1].get('processors') or call[0][1] for call in execute_processor.call_args_list]
        actual_dryruns = [call[1].get('dryrun') or call[0][2] for call in execute_processor.call_args_list]
        
        assert actual_steps == [
            {'processor': 'download', 'base_url': 'http://example.com/data', 'throttle': 1000, 'output': '/tmp/data/morgues'}
        ]
        actual_processor = actual_processors[0]
        assert all(actual_processor == p for p in actual_processors), 'Each call to `execute_processor` should have passed the same processors dict'
        assert sorted(actual_processor.keys()) == [
            'morgue-splitter', 'morgues-download', 'parser'
        ]
        assert all(dryrun == False for dryrun in actual_dryruns)

    @mock.patch('core.runner.execute_processor')
    @pytest.mark.parametrize('manifest_type', ['composed', 'multiple'])
    @pytest.mark.parametrize('dryrun', [True, False])
    def test_run_app_multiple_single_step_jobs(self, execute_processor, manifest_type, dryrun, app_manifest_composed_job, app_manifest_multiple_jobs, processors_fixtures_path):
        manifest_yaml = app_manifest_composed_job if manifest_type == 'composed' else app_manifest_multiple_jobs
        manifest = parse_yaml(manifest_yaml)
        runner.run_app(manifest, dryrun=dryrun, processors_repo_path=processors_fixtures_path)

        assert execute_processor.call_count == 2, '`execute_processor` was called an unexpected number of times'
        actual_steps = [call[1].get('step') or call[0][0] for call in execute_processor.call_args_list]
        actual_processors = [call[1].get('processors') or call[0][1] for call in execute_processor.call_args_list]
        actual_dryruns = [call[1].get('dryrun') or call[0][2] for call in execute_processor.call_args_list]
        
        assert actual_steps == [
            {'processor': 'download', 'base_url': 'http://example.com/data', 'throttle': 1000, 'output': '/tmp/data/morgues'},
            {'processor': 'splitter', 'morgues': '/tmp/data/morgues', 'output': '/tmp/data/splits'}
        ]
        actual_processor = actual_processors[0]
        assert all(actual_processor == p for p in actual_processors), 'Each call to `execute_processor` should have passed the same processors dict'
        assert sorted(actual_processor.keys()) == [
            'morgue-splitter', 'morgues-download', 'parser'
        ]
        assert all(actual_dryrun == dryrun for actual_dryrun in actual_dryruns), 'Unexpected dryruns: {}'.format(list(actual_dryruns))
  
    @mock.patch('core.runner.execute_processors')
    def test_run_app_one_job_multiple_steps(self, execute_processors, app_manifest_composed_job, processors_fixtures_path):
        manifest = parse_yaml(app_manifest_composed_job)
        runner.run_app(manifest, processors_repo_path=processors_fixtures_path)

        assert execute_processors.call_count == 1, '`execute_processors` was called an unexpected number of times'
        actual_steps = [call[1].get('step') or call[0][0] for call in execute_processors.call_args_list]
        actual_processors = [call[1].get('processors') or call[0][1] for call in execute_processors.call_args_list]
        actual_dryruns = [call[1].get('dryrun') or call[0][2] for call in execute_processors.call_args_list]
        assert actual_steps == [
            [
                {'processor': 'download', 'base_url': 'http://example.com/data', 'throttle': 1000, 'output': '/tmp/data/morgues'},
                {'processor': 'splitter', 'morgues': '/tmp/data/morgues', 'output': '/tmp/data/splits'}
            ]
        ]
        actual_processor = actual_processors[0]
        assert all(actual_processor == p for p in actual_processors), 'Each call to `execute_processor` should have passed the same processors dict'
        assert sorted(actual_processor.keys()) == [
            'morgue-splitter', 'morgues-download', 'parser'
        ]
        assert all(actual_dryrun == False for actual_dryrun in actual_dryruns), 'Unexpected dryruns: {}'.format(list(actual_dryruns))
