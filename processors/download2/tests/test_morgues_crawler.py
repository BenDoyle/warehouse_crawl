import pytest
import mock
import requests
import os
import re
from requests_mock import Adapter

from run import MorguesCrawler
    
FIXTURES_ROOT = os.path.dirname(__file__) + '/fixtures/'

@pytest.fixture
def all_morgue_files():
    return [
        'morgue-13572468-20190226-180900.txt',
        'morgue-13572468-20190226-183435.txt',
        'morgue-13572468-20190227-060836.txt',
        'morgue-assalt-20190226-180900.txt',
        'morgue-assalt-20190226-183435.txt',
        'morgue-assalt-20190227-060836.txt',
        'morgue-azanya-20190226-180900.txt',
        'morgue-azanya-20190226-183435.txt',
        'morgue-azanya-20190227-060836.txt'
    ]

@pytest.fixture
def morgue_requests_mock(requests_mock, all_morgue_files):
    def load_fixture(request, context):
        try:
            context.status_code = 200
            context.reason = 'OK'
            path = request.path[len('/morgues-repo/'):].rstrip('/') or 'root'
            if os.path.basename(path).lower() in all_morgue_files:
                return '<game data here>'
            fixture = '{}{}_listing.html'.format(FIXTURES_ROOT, path)
            if os.path.exists(fixture):
                with open(fixture, 'r') as f:
                    body = f.read()
                return body
            context.status_code = 404
            context.reason = 'Fixture {} Not Found'.format(fixture)
            return 'Not found'
        except Exception as e:
            context.status_code = 500
            context.reason = 'Exception'
            return 'Error: {}'.format(str(e))
    
    requests_mock.get(re.compile('http://example.com/morgues-repo/.*'), text=load_fixture)
    return requests_mock

@pytest.fixture
def create_crawler(morgue_requests_mock, tmpdir):
    def create(base_url='http://example.com/morgues-repo/', output=str(tmpdir), throttle=None, force=False):
        return MorguesCrawler(base_url, output, throttle, force)
    return create

@pytest.fixture
def crawler(create_crawler, requests_mock):
    return create_crawler()


def test_full_run(crawler, requests_mock, all_morgue_files):
    "Test that all files are downloaded when the output does not contain any files"
    crawler.run()

    request_history = [(r.method, r.url) for r in requests_mock.request_history]
    assert request_history == [
        ('GET', 'http://example.com/morgues-repo/'), 
        ('GET', 'http://example.com/morgues-repo/13572468/'), 
        ('GET', 'http://example.com/morgues-repo/13572468/morgue-13572468-20190226-180900.txt'), 
        ('GET', 'http://example.com/morgues-repo/13572468/morgue-13572468-20190226-183435.txt'), 
        ('GET', 'http://example.com/morgues-repo/13572468/morgue-13572468-20190227-060836.txt'), 
        ('GET', 'http://example.com/morgues-repo/Assalt/'), 
        ('GET', 'http://example.com/morgues-repo/Assalt/morgue-Assalt-20190226-180900.txt'), 
        ('GET', 'http://example.com/morgues-repo/Assalt/morgue-Assalt-20190226-183435.txt'), 
        ('GET', 'http://example.com/morgues-repo/Assalt/morgue-Assalt-20190227-060836.txt'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/morgue-Azanya-20190226-180900.txt'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/morgue-Azanya-20190226-183435.txt'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/morgue-Azanya-20190227-060836.txt')
    ], 'Unexpected HTTP request sequence'

    actual_files = sorted(f.lower() for f in os.listdir(crawler.output))
    expected_files = sorted(all_morgue_files)
    assert actual_files == expected_files, 'Unexpected output files'

def test_partial_run(crawler, requests_mock, all_morgue_files):
    existing_files = [f for f in all_morgue_files if 'assalt' in f.lower()]
    for file_ in  existing_files:
        with open('{}/{}'.format(crawler.output, file_), 'w') as fd:
            fd.write('this is an existing file')
    
    crawler.run()

    request_history = [(r.method, r.url) for r in requests_mock.request_history]
    assert request_history == [
        ('GET', 'http://example.com/morgues-repo/'), 
        ('GET', 'http://example.com/morgues-repo/13572468/'), 
        ('GET', 'http://example.com/morgues-repo/13572468/morgue-13572468-20190226-180900.txt'), 
        ('GET', 'http://example.com/morgues-repo/13572468/morgue-13572468-20190226-183435.txt'), 
        ('GET', 'http://example.com/morgues-repo/13572468/morgue-13572468-20190227-060836.txt'), 
        ('GET', 'http://example.com/morgues-repo/Assalt/'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/morgue-Azanya-20190226-180900.txt'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/morgue-Azanya-20190226-183435.txt'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/morgue-Azanya-20190227-060836.txt')
    ], 'Unexpected HTTP request sequence'

def test_forced_run(create_crawler, requests_mock, all_morgue_files):
    crawler = create_crawler(force=True)

    existing_files = [f for f in all_morgue_files if 'assalt' in f.lower()]
    for file_ in  existing_files:
        with open('{}/{}'.format(crawler.output, file_), 'w') as fd:
            fd.write('this is an existing file')
    
    crawler.run()

    request_history = [(r.method, r.url) for r in requests_mock.request_history]
    assert request_history == [
        ('GET', 'http://example.com/morgues-repo/'), 
        ('GET', 'http://example.com/morgues-repo/13572468/'), 
        ('GET', 'http://example.com/morgues-repo/13572468/morgue-13572468-20190226-180900.txt'), 
        ('GET', 'http://example.com/morgues-repo/13572468/morgue-13572468-20190226-183435.txt'), 
        ('GET', 'http://example.com/morgues-repo/13572468/morgue-13572468-20190227-060836.txt'), 
        ('GET', 'http://example.com/morgues-repo/Assalt/'), 
        ('GET', 'http://example.com/morgues-repo/Assalt/morgue-Assalt-20190226-180900.txt'), 
        ('GET', 'http://example.com/morgues-repo/Assalt/morgue-Assalt-20190226-183435.txt'), 
        ('GET', 'http://example.com/morgues-repo/Assalt/morgue-Assalt-20190227-060836.txt'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/morgue-Azanya-20190226-180900.txt'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/morgue-Azanya-20190226-183435.txt'), 
        ('GET', 'http://example.com/morgues-repo/Azanya/morgue-Azanya-20190227-060836.txt')
    ], 'Unexpected HTTP request sequence'

@mock.patch('time.sleep')
def test_throttled_run(sleep_mock, create_crawler, requests_mock, all_morgue_files):
    "Test that all files are downloaded when the output does not contain any files"
    crawler = create_crawler(throttle='10000')
    crawler.run()

    sleeps = [call[0][0] for call in sleep_mock.call_args_list]
    assert all(sleep > 9 for sleep in sleeps), 'Each throttle should have slept more than 9 seconds'
    
    request_history = [(r.method, r.url) for r in requests_mock.request_history]
    assert len(sleeps) == len(request_history) - 1, 'All but the first request should have triggered a throttle'

    actual_files = sorted(f.lower() for f in os.listdir(crawler.output))
    expected_files = sorted(all_morgue_files)
    assert actual_files == expected_files, 'Unexpected output files'
