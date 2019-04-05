import requests
import re
import os
from datetime import datetime, timedelta
import time

from lxml import html

def _get_url(url):
    response = requests.get(url)
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

    # def get_user_names(self):
    #     print('> Listing user directories at {}'.format(self.base_url))
    #     html = self._get_url(self.base_url).text
    #     usernames = _get_links(html, '<a href="([a-zA-Z0-9][^"]*)/"', group=0)
    #     for username in usernames:
    #         yield username

    # def get_user_listing(self, username):
    #     print('> Listing morgue files for [{}]'.format(username))
    #     html = self._get_url('{}{}/'.format(self.base_url, username)).text
    #     files = _get_links(html, '<a href="(morgue-[^"]*.txt)"')
    #     for file_ in files:
    #         yield '{}{}/{}'.format(self.base_url, username, file_)

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
        return _get_url(url)

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
        # for username in self.get_user_names():
        #     for file in self.get_user_listing(username):
        #         self.download(file)
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
