import os
import subprocess
import pytest
import mock
from distutils.dir_util import copy_tree  # pylint: disable=no-name-in-module, import-error
import re
import yaml

from core import runner

def parse_yaml(yaml_str):
    return yaml.load(yaml_str, yaml.FullLoader)

@pytest.fixture
def transforms_fixtures_path():
    return os.path.abspath(os.path.dirname(__file__)+'/../../tests/fixtures/')

@pytest.fixture
def simple_transform_manifest_yml():
    return """
name: simple-transform
type: transform
env-type: python
run-command: python run.py
test-command: py.test
    """

@pytest.fixture
def data_path(tmpdir):
    return os.path.join(str(tmpdir), 'data')

class TestManifestDiscovery(object):
    def test_discover_manifests_transforms(self, transforms_fixtures_path):
        transforms, _ = runner.discover_manifests(transforms_fixtures_path)

        names_and_paths = [
            (name, transform['path'])
            for name, transform in transforms.items()
        ]
        
        assert sorted(names_and_paths) == sorted([
            ('morgue-splitter', '{repo_dir}/transforms/splitter'.format(repo_dir=transforms_fixtures_path)),
            ('morgues-download', '{repo_dir}/transforms/download'.format(repo_dir=transforms_fixtures_path)),
            ('parser', '{repo_dir}/transforms/parser'.format(repo_dir=transforms_fixtures_path))
        ])

    def test_discover_manifests_publishers(self, transforms_fixtures_path):
        _, publishers = runner.discover_manifests(transforms_fixtures_path)

        names_and_paths = [
            (name, publisher['path'])
            for name, publisher in publishers.items()
        ]

        assert sorted(names_and_paths) == sorted([
            ('named-publisher', '{repo_dir}/publishers/named'.format(repo_dir=transforms_fixtures_path)),
            ('publisher-sqlite', '{repo_dir}/publishers/sqlite'.format(repo_dir=transforms_fixtures_path)),
        ])

    def test_discover_manifests_ignore_dirs_without_manifests(self, transforms_fixtures_path, tmpdir):
        repo_dir = str(tmpdir.mkdir('transforms'))
        copy_tree(transforms_fixtures_path, repo_dir)
        
        os.mkdir(os.path.join(repo_dir, 'not-a-transform'))
        with open(os.path.join(repo_dir, 'not-a-transform', 'manifest'), 'w') as fd:
            fd.write('not really a manifest')

        transforms, _ = runner.discover_manifests(repo_dir)

        assert sorted(transforms.keys()) == sorted([
            'morgue-splitter', 'morgues-download', 'parser'
        ])

    @mock.patch('core.runner.load_manifest_at_path')
    def test_discover_manifests_ignore_test_dirs(self, load_manifest_at_path, transforms_fixtures_path, simple_transform_manifest_yml, tmpdir):
        repo_dir = tmpdir.mkdir('manifests')
        tests_dir = repo_dir.mkdir('transforms').mkdir('parser').mkdir('tests')
        nested_tests_dir = tests_dir.mkdir('nested').mkdir('deeply')

        copy_tree(transforms_fixtures_path, str(repo_dir))

        for path in [tests_dir, nested_tests_dir]:
            with open(os.path.join(str(path), 'manifest.yml'), 'w') as fd:
                fd.write(simple_transform_manifest_yml)
        
        runner.discover_manifests(repo_dir)

        loaded_paths = [c[0][0] for c in load_manifest_at_path.call_args_list]
        assert tests_dir not in loaded_paths, 'the "tests" directory was not skipped'
        assert nested_tests_dir not in loaded_paths, 'the nested "tests" directory was not skipped'

    def test_discover_manifests_ignore_invalid_yaml_manifest(self, transforms_fixtures_path, tmpdir):
        repo_dir = str(tmpdir.mkdir('transforms'))
        copy_tree(transforms_fixtures_path, repo_dir)
        
        os.mkdir(os.path.join(repo_dir, 'invalid-yaml-transform'))
        with open(os.path.join(repo_dir, 'invalid-yaml-transform', 'manifest.yml'), 'w') as fd:
            fd.write('not really a manifest')

        transforms, _ = runner.discover_manifests(repo_dir)

        assert sorted(transforms.keys()) == sorted([
            'morgue-splitter', 'morgues-download', 'parser'
        ])

    @pytest.mark.parametrize('required_key', [
        'name', 'run-command'
    ])
    def test_discover_manifests_ignore_missing_required_transform_field(self, required_key, transforms_fixtures_path, tmpdir):
        repo_dir = str(tmpdir.mkdir('transforms'))
        copy_tree(transforms_fixtures_path, repo_dir)
        
        yaml = re.sub(r'^([ \t]*{}\:)'.format(required_key), r'# \1', """
name: invalid-manifest-transform
type: transform
run-command: python run.py
        """, flags=re.MULTILINE)
        os.mkdir(os.path.join(repo_dir, 'invalid-transform'))
        with open(os.path.join(repo_dir, 'invalid-transform', 'manifest.yml'), 'w') as fd:
            fd.write(yaml)

        transforms, _ = runner.discover_manifests(repo_dir)

        assert sorted(transforms.keys()) == [
            'morgue-splitter', 'morgues-download', 'parser'
        ]
    
    @pytest.mark.parametrize('required_key', [
        'output-type'
    ])
    def test_discover_manifests_ignore_missing_required_publisher_field(self, required_key, transforms_fixtures_path, tmpdir):
        repo_dir = str(tmpdir.mkdir('transforms'))
        copy_tree(transforms_fixtures_path, repo_dir)
        
        yaml = re.sub(r'^([ \t]*{}\:)'.format(required_key), r'# \1', """
type: publisher
output-type: sqlite
run-command: python run.py
        """, flags=re.MULTILINE)
        os.mkdir(os.path.join(repo_dir, 'invalid-transform'))
        with open(os.path.join(repo_dir, 'invalid-transform', 'manifest.yml'), 'w') as fd:
            fd.write(yaml)

        _, publishers = runner.discover_manifests(repo_dir)

        assert sorted(publishers.keys()) == [
            'named-publisher', 'publisher-sqlite'
        ]

@mock.patch('subprocess.run', mock.Mock())
class TestAppManifest(object):

    @pytest.fixture
    def app_manifest_simple(self, data_path):
        return """
name: Simple app manifest
data: {data_path}
jobs:
  my-job:
    - transform: download
      base_url: http://example.com/data
      throttle: 1000
        """.format(data_path=data_path)

    @pytest.fixture
    def app_manifest_simple_published(self, app_manifest_simple):
        return """{simple_manifest}
    - publish-to: /published/path
      type: sqlite
        """.format(simple_manifest=app_manifest_simple)

    @pytest.fixture
    def app_manifest_multiple_single_step_jobs(self, data_path):
        return """
name: Multiple job manifest
data: {data_path}
jobs:
  download:
    - transform: download
      base_url: http://example.com/data
      throttle: 1000
  split:
    - transform: splitter
      morgues: /tmp/data/morgues
        """.format(data_path=data_path)

    @pytest.fixture
    def app_manifest_single_multiple_step_job(self, data_path):
        return """
name: Multiple job manifest
data: {data_path}
jobs:
  download:
    - transform: download
      base_url: http://example.com/data
      throttle: 1000
    - transform: splitter
      morgues: /tmp/data/morgues
        """.format(data_path=data_path)

    @mock.patch('core.runner.execute_transform')
    def test_run_app_simple_job(self, execute_transform, app_manifest_simple, transforms_fixtures_path):
        manifest = parse_yaml(app_manifest_simple)
        runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert execute_transform.call_count == 1, '`execute_transform` was called an unexpected number of times'
        actual_steps = [call[1].get('step') or call[0][0] for call in execute_transform.call_args_list]
        actual_transforms = [call[1].get('transforms') or call[0][1] for call in execute_transform.call_args_list]
        actual_dryruns = [call[1].get('dryrun') or call[0][2] for call in execute_transform.call_args_list]
        
        assert actual_steps == [
            {'transform': 'download', 'base_url': 'http://example.com/data', 'throttle': 1000, 'output': mock.ANY}
        ]
        actual_transform = actual_transforms[0]
        assert all(actual_transform == p for p in actual_transforms), 'Each call to `execute_transform` should have passed the same transforms dict'
        assert sorted(actual_transform.keys()) == [
            'morgue-splitter', 'morgues-download', 'parser'
        ]
        assert all(dryrun == False for dryrun in actual_dryruns)

    @mock.patch('core.runner.execute_transform')
    @pytest.mark.parametrize('dryrun', [True, False])
    def test_run_app_multiple_single_step_jobs(self, execute_transform, dryrun, app_manifest_multiple_single_step_jobs, transforms_fixtures_path):
        manifest = parse_yaml(app_manifest_multiple_single_step_jobs)
        runner.run_app(manifest, dryrun=dryrun, transforms_repo_path=transforms_fixtures_path)

        # TODO review this test, we might need to verify that execute_job_steps is called twice instead
        assert execute_transform.call_count == 2, '`execute_transform` was called an unexpected number of times'
        actual_steps = [call[1].get('step') or call[0][0] for call in execute_transform.call_args_list]
        actual_transforms = [call[1].get('transforms') or call[0][1] for call in execute_transform.call_args_list]
        actual_dryruns = [call[1].get('dryrun') or call[0][2] for call in execute_transform.call_args_list]
        
        assert actual_steps == [
            {'transform': 'download', 'base_url': 'http://example.com/data', 'throttle': 1000, 'output': mock.ANY},
            {'transform': 'splitter', 'morgues': mock.ANY, 'output': mock.ANY}
        ]
        actual_transform = actual_transforms[0]
        assert all(actual_transform == p for p in actual_transforms), 'Each call to `execute_transform` should have passed the same transforms dict'
        assert sorted(actual_transform.keys()) == [
            'morgue-splitter', 'morgues-download', 'parser'
        ]
        assert all(actual_dryrun == dryrun for actual_dryrun in actual_dryruns), 'Unexpected dryruns: {}'.format(list(actual_dryruns))

    @mock.patch('core.runner.execute_publish')
    @mock.patch('core.runner.execute_transform')
    def test_run_app_publish(self, execute_transform, execute_publish, app_manifest_simple_published, transforms_fixtures_path):
        manifest = parse_yaml(app_manifest_simple_published)
        runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert execute_publish.call_count == 1, '`execute_publish` was called an unexpected number of times'
        
        actual_steps = [call[1].get('step') or call[0][0] for call in execute_publish.call_args_list]
        actual_publishers = [call[1].get('transforms') or call[0][1] for call in execute_publish.call_args_list]
        actual_dryruns = [call[1].get('dryrun') or call[0][2] for call in execute_publish.call_args_list]
        
        assert actual_steps == [
            {'publish-to': '/published/path', 'type': 'sqlite'}
        ]
        actual_publisher = actual_publishers[0]
        assert all(actual_publisher == p for p in actual_publishers), 'Each call to `execute_publisher` should have passed the same publishers dict'
        assert sorted(actual_publisher.keys()) == [
            'named-publisher', 'publisher-sqlite'
        ]
        assert all(dryrun == False for dryrun in actual_dryruns)

    @mock.patch('core.runner.execute_publish')
    @mock.patch('core.runner.execute_transform')
    def test_run_app_publish_must_be_last_step(self, execute_transform, execute_publish, app_manifest_simple_published, transforms_fixtures_path):
        yaml = app_manifest_simple_published + """
    - transform: splitter
      morgues: /tmp/data/morgues
        """
        manifest = parse_yaml(yaml)

        with pytest.raises(AssertionError) as exc_info:
            runner.run_app(manifest)
    
        assert str(exc_info.value) == 'The publish step for job "my-job" cannot be followed by subsequent steps'

    @mock.patch('core.runner.execute_job_steps')
    def test_run_app_one_job_multiple_steps(self, execute_job_steps, app_manifest_single_multiple_step_job, transforms_fixtures_path):
        manifest = parse_yaml(app_manifest_single_multiple_step_job)
        runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert execute_job_steps.call_count == 1, '`execute_job_steps` was called an unexpected number of times'
        actual_job_name = [call[1].get('step') or call[0][0] for call in execute_job_steps.call_args_list]
        actual_steps = [call[1].get('step') or call[0][1] for call in execute_job_steps.call_args_list]
        actual_transforms = [call[1].get('transforms') or call[0][2] for call in execute_job_steps.call_args_list]
        actual_publishers = [call[1].get('publishers') or call[0][3] for call in execute_job_steps.call_args_list]
        actual_dryruns = [call[1].get('dryrun') or call[0][4] for call in execute_job_steps.call_args_list]
        assert actual_job_name == ['download']
        assert actual_steps == [
            [
                {'transform': 'download', 'base_url': 'http://example.com/data', 'throttle': 1000, 'output': mock.ANY},
                {'transform': 'splitter', 'morgues': mock.ANY, 'output': mock.ANY}
            ]
        ]
        actual_transform = actual_transforms[0]
        actual_publisher = actual_publishers[0]
        assert all(actual_transform == p for p in actual_transforms), 'Each call to `execute_transform` should have passed the same transforms dict'
        assert all(actual_publisher == p for p in actual_publishers), 'Each call to `execute_transform` should have passed the same publishers dict'
        assert sorted(actual_transform.keys()) == [
            'morgue-splitter', 'morgues-download', 'parser'
        ]
        assert all(actual_dryrun == False for actual_dryrun in actual_dryruns), 'Unexpected dryruns: {}'.format(list(actual_dryruns))

    @mock.patch('core.runner.execute_transform')
    @mock.patch('core.runner.temp_directory', return_value='/data/tmp/dir')
    @mock.patch('core.runner.temp_file', return_value='/data/tmp/file')
    def test_run_app_temp_placeholder(self, tmpfile_mock, tmpdir_mock, execute_transform, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Named placeholder
data: {data_path}
jobs:
  my-job:
    - transform: morgues-download
      some-file: $tmp.file
      output: $tmp.dir
        """.format(data_path=data_path))
        runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert execute_transform.call_count == 1, '`execute_transform` was called an unexpected number of times'
        actual_steps = [call[1].get('step') or call[0][0] for call in execute_transform.call_args_list]
        assert actual_steps == [
            {'transform': 'morgues-download', 'some-file': '/data/tmp/file', 'output': mock.ANY},
        ]

    @mock.patch('core.runner.execute_transform')
    def test_run_app_named_placeholders(self, execute_transform, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  my-job:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
      throttle: 1000
    - transform: morgue-splitter
      morgues: $downloader.output  # this should be replaced with the first step's output value
        """.format(data_path=data_path))
        runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert execute_transform.call_count == 2, '`execute_transform` was called an unexpected number of times'
        actual_steps = [call[1].get('step') or call[0][0] for call in execute_transform.call_args_list]
        assert actual_steps[1]['morgues'] == actual_steps[0]['output']

    @mock.patch('core.runner.execute_transform')
    def test_run_app_named_placeholders_step_name_not_found(self, execute_transform, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  my-job:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
      throttle: 1000
    - transform: morgue-splitter
      morgues: $unknown.output  # unknown step name
        """.format(data_path=data_path))

        with pytest.raises(AssertionError) as exc:
            runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert str(exc.value) == "Invalid placeholder: $unknown; valid names include: ['downloader']"
        

    @mock.patch('core.runner.execute_transform')
    def test_run_app_named_placeholders_value_key_not_found(self, execute_transform, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  my-job:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
      throttle: 1000
    - transform: morgue-splitter
      morgues: $downloader.unknown  # unknown value name
        """.format(data_path=data_path))

        with pytest.raises(AssertionError) as exc:
            runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert str(exc.value) == "Invalid placeholder: $downloader.unknown; valid option names include: ['base_url', 'name', 'output', 'throttle', 'transform']"

    @mock.patch('core.runner.execute_transform')
    def test_run_app_named_placeholders_reference_future_step(self, execute_transform, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  my-job:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
      throttle: 1000
      output: $splitter.morgues  # cannot reference values from future steps
    - name: splitter
      transform: /tmp/data/morgues
      morgues: $downloader.unknown
      output: /tmp/data/splits
        """.format(data_path=data_path))

        with pytest.raises(AssertionError) as exc:
            runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert str(exc.value) == "Invalid placeholder: $splitter; valid names include: []"

    @mock.patch('core.runner.execute_transform')
    def test_run_app_named_placeholders_reference_other_job(self, execute_transform, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  job1:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
      throttle: 1000
  job2:
    - transform: morgue-splitter
      morgues: $downloader.output  # not part of the same job
        """.format(data_path=data_path))

        with pytest.raises(AssertionError) as exc:
            runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert str(exc.value) == "Invalid placeholder: $downloader; valid names include: []"

    @mock.patch('core.runner.execute_job_steps')
    def test_run_app_named_placeholders_circular_reference(self, execute_job_steps, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  job1:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
      throttle: 1000
      output: $splitter.output
    - name: splitter
      transform: morgue-splitter
      morgues: morgues
      output: $downloader.output
        """.format(data_path=data_path))

        with pytest.raises(AssertionError) as exc:
            runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert str(exc.value) == "Invalid placeholder: $splitter; valid names include: []"

    @mock.patch('core.runner.execute_job_steps')
    def test_run_app_chained_placeholders(self, execute_job_steps, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  job1:
    - name: downloader1
      transform: morgues-download
      base_url: http://example.com/data
    - name: downloader2
      transform: morgues-download
      base_url: $downloader1.base_url
    - name: downloader3
      transform: morgues-download
      base_url: $downloader2.base_url
        """.format(data_path=data_path))

        runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert execute_job_steps.call_count == 1
        actual_steps = execute_job_steps.call_args_list[0][1].get('steps') or execute_job_steps.call_args_list[0][0][1]        
        actual_base_urls = [step['base_url'] for step in actual_steps]
        assert actual_base_urls == ['http://example.com/data'] * 3

    @mock.patch('core.runner.execute_job_steps')
    def test_resolve_tmp_dir(self, execute_job_steps, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  job1:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
      output: $tmp.dir
    - name: splitter
      transform: morgue-splitter
      morgues: morgues
      output: $downloader.output
        """.format(data_path=data_path))

        runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert execute_job_steps.call_count == 1
        actual_steps = execute_job_steps.call_args_list[0][1].get('steps') or execute_job_steps.call_args_list[0][0][1]        
        assert all(step['output'] == actual_steps[0]['output'] for step in actual_steps), 'Every tmp value should be the same value'
        assert actual_steps[0]['output'].startswith(data_path + '/tmp/')
        assert os.path.isdir(actual_steps[0]['output'])
    
    @mock.patch('core.runner.execute_job_steps')
    def test_resolve_tmp_file(self, execute_job_steps, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  job1:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
      output: $tmp.file
    - name: splitter
      transform: morgue-splitter
      morgues: morgues
      output: $downloader.output
        """.format(data_path=data_path))

        runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert execute_job_steps.call_count == 1
        actual_steps = execute_job_steps.call_args_list[0][1].get('steps') or execute_job_steps.call_args_list[0][0][1]        
        assert all(step['output'] == actual_steps[0]['output'] for step in actual_steps), 'Every tmp value should be the same value'
        assert actual_steps[0]['output'].startswith(data_path + '/tmp/')
        assert os.path.isfile(actual_steps[0]['output'])

    @mock.patch('core.runner.execute_job_steps')
    @pytest.mark.parametrize('placeholder, resolved', [
        ('${downloader.output}/mid/${downloader.name}', '/some/path/mid/downloader'),
        ('[${downloader.output}${downloader.name}]', '[/some/pathdownloader]'),
        ('${downloader.output}$downloader.name', '/some/path$downloader.name'),
    ])
    def test_resolve_variable_curley_braces(self, execute_job_steps, placeholder, resolved, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  job1:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
      output: /some/path
    - name: splitter
      transform: morgue-splitter
      morgues: morgues
      output: '{placeholder}'
        """.format(data_path=data_path, placeholder=placeholder))

        runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert execute_job_steps.call_count == 1
        actual_steps = execute_job_steps.call_args_list[0][1].get('steps') or execute_job_steps.call_args_list[0][0][1]        
        assert actual_steps[1]['output'] == resolved

    @mock.patch('core.runner.execute_job_steps')
    def test_resolve_variable_previous_output(self, execute_job_steps, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  job1:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
    - name: splitter
      transform: morgue-splitter
      morgues: $previous.output
    - publish-to: /final/output
      type: sqlite
    #   data: $previous.output  -- not necessary, should always be the previous output
        """.format(data_path=data_path))

        runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert execute_job_steps.call_count == 1
        actual_steps = execute_job_steps.call_args_list[0][1].get('steps') or execute_job_steps.call_args_list[0][0][1]        
        assert actual_steps[1]['morgues'] == actual_steps[0]['output']

    @mock.patch('core.runner.execute_job_steps')
    def test_resolve_variable_previous_output_no_previous_output(self, execute_job_steps, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  job1:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
    - name: splitter
      transform: morgue-splitter
      morgues: $previous.not_defined
        """.format(data_path=data_path))

        with pytest.raises(Exception) as exc_info:
            runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)
        assert str(exc_info.value) == 'No previous value found for $previous.not_defined (previous == "downloader")'

    @mock.patch('core.runner.execute_job_steps')
    def test_resolve_variable_previous_output_first_step(self, execute_job_steps, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  job1:
    - name: splitter
      transform: morgue-splitter
      morgues: $previous.output
        """.format(data_path=data_path))

        with pytest.raises(Exception) as exc_info:
            runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)
        assert str(exc_info.value) == 'Cannot use $previous placeholder on the first step'

    @mock.patch('core.runner.execute_job_steps')
    def test_resolve_variable_previous_output_variable(self, execute_job_steps, transforms_fixtures_path, data_path):
        manifest = parse_yaml("""
name: Single composed job manifest
data: {data_path}
jobs:
  job1:
    - name: downloader
      transform: morgues-download
      base_url: http://example.com/data
    - name: splitter
      transform: morgue-splitter
      morgues: $previous.output
        """.format(data_path=data_path))

        runner.run_app(manifest, transforms_repo_path=transforms_fixtures_path)

        assert execute_job_steps.call_count == 1
        actual_steps = execute_job_steps.call_args_list[0][1].get('steps') or execute_job_steps.call_args_list[0][0][1]        
        assert actual_steps[1]['morgues'] == actual_steps[0]['output']
        assert actual_steps[0]['output'].startswith(data_path)

    @pytest.mark.skip('TODO')
    def test_execute_transform(self):
        assert subprocess.run.call_count == 100
        assert False, 'need to test the implementation of execute_transform'

    @pytest.mark.skip('TODO')
    def test_execute_publish(self):
        assert subprocess.run.call_count == 100
        assert False, 'need to test the implementation of execute_publish'