import requests
import re
import os

BASE_URL = 'http://crawl.develz.org/morgues/0.23/'

def __get_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def __get_links(html, pattern, group=0):
    pattern = re.compile(pattern)
    for link in pattern.findall(html):
        yield link

def get_user_names():
    print('> Listing user directories at {}'.format(BASE_URL))
    html = __get_url(BASE_URL)
    usernames = __get_links(html, '<a href="([a-zA-Z0-9][^"]*)/"', group=0)
    for username in usernames:
        yield username

def get_user_listing(username):
    print('> Listing morgue files for [{}]'.format(username))
    html = __get_url('{}{}/'.format(BASE_URL, username))
    files = __get_links(html, '<a href="(morgue-[^"]*.txt)"')
    for file_ in files:
        yield '{}{}/{}'.format(BASE_URL, username, file_)

def download(file_):
    print('  > Downloading {} ...'.format(os.path.basename(file_)))
    response = requests.get(file_)
    if not response.ok:
        print('  !! Failed to download file {} {} - {}'.format(response.status_code, response.reason, file_))
        return

    basedir = './{}/morgue'.format(os.path.dirname(__file__))
    filepath = './{}/morgue/{}'.format(os.path.dirname(__file__), os.path.basename(file_))
    if not os.path.exists(basedir):
        os.mkdir(basedir, exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(response.content)

if __name__ == '__main__':
    usernames = get_user_names()

    for username in get_user_names():
        for file in get_user_listing(username):
            download(file)
