import pytest
import mock
import requests
import os
import pathlib
import re
from datetime import datetime, timedelta
from requests_mock import Adapter

from run import MorguesCrawler

FIXTURES_ROOT = os.path.dirname(__file__) + '/fixtures/'

def _get_downloaded_files(output_path):
    return sorted(
        str(f)[len(output_path)+1:].lower()
        for f in pathlib.Path(output_path).glob('**/morgue-*.txt')
    )

def _write_existing_files(existing_files, output_path):
    for file_ in  existing_files:
        dirname = '{}/{}'.format(output_path, os.path.dirname(file_))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open('{}/{}'.format(output_path, file_), 'w') as fd:
            fd.write('this is an existing file')

@pytest.fixture
def all_morgue_files():
    return [
        'abaeterno/morgue-abaeterno-20190828-000758.txt',
        '0beahy/morgue-0beahy-20190829-201557.txt',
        '0beahy/morgue-0beahy-20190829-201920.txt',
        'nonames/morgue-nonames-20190216-225551.txt',
        'nonames/morgue-nonames-20190216-230702.txt',
        'nonames/morgue-nonames-20190216-232003.txt',
        'nonames/morgue-nonames-20190216-235627.txt',
        'nonames/morgue-nonames-20190217-000644.txt',
        'nonames/morgue-nonames-20190217-001554.txt',
        'nonames/morgue-nonames-20190217-002546.txt',
        'nonames/morgue-nonames-20190217-003006.txt',
        'nonames/morgue-nonames-20190217-003902.txt',
        'nonames/morgue-nonames-20190217-004619.txt',
        'nonames/morgue-nonames-20190217-005701.txt',
        'nonames/morgue-nonames-20190217-010755.txt',
        'nonames/morgue-nonames-20190217-011446.txt',
        'nonames/morgue-nonames-20190217-011931.txt',
        'nonames/morgue-nonames-20190217-012807.txt',
        'nonames/morgue-nonames-20190813-070904.txt',
        'nonames/morgue-nonames-20190813-073811.txt',
    ]

@pytest.fixture
def morgue_requests_mock(requests_mock, all_morgue_files):
    def load_fixture(request, context):
        try:
            context.status_code = 200
            context.reason = 'OK'
            path = request.path[len('/morgues-repo/'):].rstrip('/') or 'root'
            if os.path.basename(path) in [os.path.basename(p) for p in all_morgue_files]:
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
def output_path(tmpdir):
    return str(tmpdir)

@pytest.fixture
def create_crawler(request, morgue_requests_mock, output_path):
    mocks = {} if 'real_io' in request.keywords else {
        'has_updated_morgues': mock.Mock(return_value=True),
        '_record_last_crawl': mock.Mock(),
    }
    with mock.patch.multiple('run.MorguesCrawler', **mocks) if mocks else mock.MagicMock():
        def create(base_url='http://example.com/morgues-repo/', output=output_path, throttle=None, force=False):
            return MorguesCrawler(base_url, output, throttle, force)
        yield create

@pytest.fixture
def crawler(create_crawler, requests_mock):
    return create_crawler()


def test_full_run(crawler, requests_mock, all_morgue_files):
    "Test that all files are downloaded when the output does not contain any files"
    crawler.run()

    request_history = [(r.method, r.url) for r in requests_mock.request_history]
    assert request_history == [('GET', 'http://example.com/morgues-repo/'),
        ('GET', 'http://example.com/morgues-repo/0beahy/'),
        ('GET', 'http://example.com/morgues-repo/0beahy/morgue-0beahy-20190829-201557.txt'),
        ('GET', 'http://example.com/morgues-repo/0beahy/morgue-0beahy-20190829-201920.txt'),
        ('GET', 'http://example.com/morgues-repo/AbAeterno/'),
        ('GET', 'http://example.com/morgues-repo/AbAeterno/morgue-AbAeterno-20190828-000758.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190216-225551.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190216-230702.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190216-232003.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190216-235627.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-000644.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-001554.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-002546.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-003006.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-003902.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-004619.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-005701.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-010755.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-011446.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-011931.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-012807.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190813-070904.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190813-073811.txt')
    ], 'Unexpected HTTP request sequence'

    actual_files = _get_downloaded_files(crawler.output)
    expected_files = sorted(all_morgue_files)
    assert actual_files == expected_files, 'Unexpected output files'

    assert crawler._record_last_crawl.call_args_list == [
        mock.call('http://example.com/morgues-repo/0beahy/', mock.ANY),
        mock.call('http://example.com/morgues-repo/AbAeterno/', mock.ANY),
        mock.call('http://example.com/morgues-repo/nonames/', mock.ANY)
    ]

def test_partial_run(crawler, requests_mock, all_morgue_files):
    up_to_date = [
        'http://example.com/morgues-repo/AbAeterno/'  # skip entirely without fetching the listing
    ]
    crawler.has_updated_morgues = lambda url, _: url not in up_to_date

    existing_files = [f for f in all_morgue_files if 'nonames' in f.lower() and f.lower() < 'nonames/morgue-nonames-20190813-070904.txt']
    _write_existing_files(existing_files, crawler.output)

    crawler.run()

    request_history = [(r.method, r.url) for r in requests_mock.request_history]
    assert request_history == [
        ('GET', 'http://example.com/morgues-repo/'),
        ('GET', 'http://example.com/morgues-repo/0beahy/'),
        ('GET', 'http://example.com/morgues-repo/0beahy/morgue-0beahy-20190829-201557.txt'),  # fetch them all
        ('GET', 'http://example.com/morgues-repo/0beahy/morgue-0beahy-20190829-201920.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190813-070904.txt'), # fetches only the last 2 files that don't exist
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190813-073811.txt')
    ], 'Unexpected HTTP request sequence'

    assert crawler._record_last_crawl.call_args_list == [
        mock.call('http://example.com/morgues-repo/0beahy/', mock.ANY),
        mock.call('http://example.com/morgues-repo/nonames/', mock.ANY)
    ]

def test_forced_run(create_crawler, requests_mock, all_morgue_files):
    crawler = create_crawler(force=True)

    existing_files = [f for f in all_morgue_files if 'nonames' in f.lower()]
    _write_existing_files(existing_files, crawler.output)

    crawler.run()

    request_history = [(r.method, r.url) for r in requests_mock.request_history]
    assert request_history == [
        ('GET', 'http://example.com/morgues-repo/'),
        ('GET', 'http://example.com/morgues-repo/0beahy/'),
        ('GET', 'http://example.com/morgues-repo/0beahy/morgue-0beahy-20190829-201557.txt'),
        ('GET', 'http://example.com/morgues-repo/0beahy/morgue-0beahy-20190829-201920.txt'),
        ('GET', 'http://example.com/morgues-repo/AbAeterno/'),
        ('GET', 'http://example.com/morgues-repo/AbAeterno/morgue-AbAeterno-20190828-000758.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190216-225551.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190216-230702.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190216-232003.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190216-235627.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-000644.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-001554.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-002546.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-003006.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-003902.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-004619.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-005701.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-010755.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-011446.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-011931.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190217-012807.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190813-070904.txt'),
        ('GET', 'http://example.com/morgues-repo/nonames/morgue-nonames-20190813-073811.txt')
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

    actual_files = _get_downloaded_files(crawler.output)
    expected_files = sorted(all_morgue_files)
    assert actual_files == expected_files, 'Unexpected output files'

def test_last_crawl_path(create_crawler, output_path):
    crawler = create_crawler()
    assert crawler._last_crawl_path('http://example.com/morgues-repo/nonames/') == '{}/nonames/.last_crawl'.format(output_path)

@pytest.mark.real_io
def test_read_write_last_crawl(create_crawler):
    last_crawl = datetime(2019, 9, 6, 1, 23)
    url = 'http://example.com/morgues-repo/nonames/'
    crawler = create_crawler()

    assert crawler.has_updated_morgues(url, last_crawl), 'File does not exist, we should assume there are updated morgues'
    crawler._record_last_crawl(url, last_crawl)

    assert crawler.has_updated_morgues(url, last_crawl), 'Updated timestamp matches the last crawl, we should check for updates just in case'
    assert crawler.has_updated_morgues(url, last_crawl + timedelta(minutes=1)), 'Updated since last crawl, we should check for updates'
    assert not crawler.has_updated_morgues(url, last_crawl - timedelta(minutes=1)), 'Has not been updated since last crawl, so do not check for updates'
