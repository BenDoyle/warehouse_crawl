import requests
import re
import os
from datetime import datetime, timedelta
import time

from lxml import html

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
        filepath = '{}/{}'.format(basedir, os.path.basename(file_))
        if not self.force and os.path.exists(filepath):
            print('  > !! Skipping existing file {} ...'.format(os.path.basename(file_)))
            return

        print('  > Downloading {} ...'.format(os.path.basename(file_)))
        response = self._get_url(file_)
        if not response.ok:
            print('  !! Failed to download file {} {} - {}'.format(response.status_code, response.reason, file_))
            return

        if not os.path.exists(basedir):
            os.makedirs(basedir)
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
        MORGUE_FILENAME_REGEX = '^morgue-.*\.txt$'

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


    def get_listing(self, url):
        print('* Downloading listing from {} ...'.format(url))
        response = self._get_url(url)
        response.raise_for_status()

        print('  > Parsing listing ...')
        doc = html.fromstring(response.text)
        links = doc.xpath('//table/tr/td[2]/a')
        for link in links:
            if not link.get('href'):
                continue
            if link.get('href').startswith('/'):
                continue # ignore, it's likely the "Parent Directory" link
            yield os.path.join(url, link.get('href'))

    def run(self):
        for user_url in self.get_listing(self.base_url):
            for morgue_url in self.get_user_morgues(user_url):
                self.download(morgue_url)



if __name__ == '__main__':
    options = ['base_url', 'output', 'force', 'throttle']
    required = ['base_url', 'output']

    env = {
        option: os.environ.get(option.upper())
        for option in options
    }
    missing_options = set(required) & set(option for option, value in env.items() if not value)
    if set(required) & set(option for option, value in env.items() if not value):
        raise Exception('Missing required options: {}'.format(missing_options))
    crawler = MorguesCrawler(**env)
    crawler.run()
