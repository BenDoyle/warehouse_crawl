import requests
import re
import os
import simplejson as json
from datetime import datetime, timedelta
import time
from datetime import datetime
from urllib.parse import urlparse

from lxml import html

BASE_URL = 'http://crawl.berotato.org/crawl/morgue/'
DATE_FORMAT = '%d-%b-%Y %H:%M'

def _get_url(url, session):
    response = session.get(url)
    response.raise_for_status()
    return response

def _get_links(html, pattern, group=0):
    pattern = re.compile(pattern)
    for link in pattern.findall(html):
        yield link

class MorguesCrawler(object):
    def __init__(self, base_url, output, throttle=None, force=False):
        self.__base_url = base_url
        self.__output = output
        self.__throttle = timedelta(milliseconds=int(throttle)) if throttle else None
        self.__force = force
        self.__last_download = datetime(2000,1,1)
        self.__cached_session = (requests.Session(), datetime.now())

    @property
    def base_url(self):
        return self.__base_url

    @property
    def output(self):
        return self.__output

    @property
    def throttle(self):
        return self.__throttle

    @property
    def force(self):
        return self.__force

    def download(self, file_):
        basedir = self.output.rstrip('/')
        basename = os.path.basename(file_)
        username = os.path.basename(os.path.dirname(file_))

        filepath = '{}/{}/{}'.format(basedir, username, basename)
        if not self.force and os.path.exists(filepath):
            print('  > !! Skipping existing file {} ...'.format(basename))
            return

        print('  > Downloading {} ...'.format(basename))
        response = self._get_url(file_)
        if not response.ok:
            print('  !! Failed to download file {} {} - {}'.format(response.status_code, response.reason, file_))
            return

        parent_dir = os.path.dirname(filepath)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(filepath, 'wb') as f:
            f.write(response.content)

    def _get_url(self, url):
        now = datetime.now()
        if self.throttle:
            delta = now - self.__last_download
            if delta < self.throttle:
                seconds = self.throttle.total_seconds() - (delta.microseconds / 1000000.0)
                print('  ! Sleeping {} seconds'.format(seconds))
                time.sleep(seconds)
        self.__last_download = now

        session, birth = self.__cached_session
        if datetime.now() - birth > timedelta(minutes=10):
            session, birth = requests.Session(), datetime.now()
            self.__cached_session = session, birth
        return _get_url(url, session)

    def get_user_morgues(self, url):
        MORGUE_FILENAME_REGEX = '^morgue-.*[.]txt$'

        current_crawl = datetime.strftime(datetime.utcnow(), DATE_FORMAT)

        print('*** Downloading user listing at {} ...'.format(url))
        response = self._get_url(url)
        response.raise_for_status()

        print('    > Parsing listing')
        doc = html.fromstring(response.text)
        links = doc.xpath('//table/tr/td[2]/a')
        morge_file_pattern = re.compile(MORGUE_FILENAME_REGEX)
        for link in links:
            if morge_file_pattern.fullmatch(link.get('href')):
                yield os.path.join(url, link.get('href'))

    def has_updated_morgues(self, url, updated_at):
        path = self._last_crawl_path(url)
        if not os.path.exists(path):
            return True
        with open(path, 'r') as f:
            last_crawl = f.readline()
        last_crawl = datetime.strptime(last_crawl, DATE_FORMAT) if last_crawl else datetime.min
        return updated_at >= last_crawl

    def _last_crawl_path(self, url):
        basename = os.path.basename(urlparse(url).path.rstrip('/'))
        return '{}/{}/.last_crawl'.format(self.__output, basename)

    def _record_last_crawl(self, url, last_crawl):
        path = self._last_crawl_path(url)
        parent_dir = os.path.dirname(path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(path, 'w') as fd:
            fd.write(datetime.strftime(last_crawl, DATE_FORMAT))

    def get_listing(self, url):
        print('* Downloading listing from {} ...'.format(url))
        response = self._get_url(url)
        response.raise_for_status()

        current_crawl = datetime.strftime(datetime.utcnow(), DATE_FORMAT)

        print('  > Parsing listing ...')
        doc = html.fromstring(response.text)
        links = doc.xpath('//table/tr/td[2]/a')
        dates = doc.xpath('//table/tr/td[3]')
        for link, date in zip(links, dates):
            if not link.get('href'):
                continue
            if link.get('href').startswith('/'):
                continue # ignore, it's likely the "Parent Directory" link

            href = os.path.join(url, link.get('href'))
            updated_at = datetime.strptime(date.text.strip(), DATE_FORMAT)
            yield href, updated_at

    def run(self):
        for user_url, updated_at in self.get_listing(self.base_url):
            if not self.has_updated_morgues(user_url, updated_at):
                continue
            current_crawl = datetime.utcnow()
            for morgue_url in self.get_user_morgues(user_url):
                self.download(morgue_url)
            self._record_last_crawl(user_url, current_crawl)



if __name__ == '__main__':
    options = ['output', 'force', 'throttle']
    required = ['output']

    env = {
        option: os.environ.get(option.upper())
        for option in options
    }
    missing_options = set(required) & set(option for option, value in env.items() if not value)
    if set(required) & set(option for option, value in env.items() if not value):
        raise Exception('Missing required options: {}'.format(missing_options))

    env['base_url'] = BASE_URL
    crawler = MorguesCrawler(**env)
    crawler.run()
