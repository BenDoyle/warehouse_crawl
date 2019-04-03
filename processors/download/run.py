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
    return pattern.findall(html)

def get_user_names():
    print('> Listing user directories at {}'.format(BASE_URL))
    html = __get_url(BASE_URL)
    usernames = __get_links(html, '<a href="([a-zA-Z0-9][^"]*)/"', group=0)
    print('  > Found {} username{}'.format(len(usernames), '' if len(usernames) == 1 else 's'))
    return usernames

def get_user_listing(username):
    print('> Listing morgue files for [{}]'.format(username))
    html = __get_url('{}{}/'.format(BASE_URL, username))
    files = __get_links(html, '<a href="(morgue-[^"]*.txt)"')
    files = [
        '{}{}/{}'.format(BASE_URL, username, file_)
        for file_ in files
    ]
    print('  > Found {} file{}'.format(len(files), '' if len(files) == 1 else 's'))

def download(files_dict):
    for username, files in sorted(files_dict.items()):
        print('Downloading {} file{} from user {}'.format(len(files), '' if len(files) == 1 else 's', username))
        for file_ in files:
            response = requests.get(file_)
            if not response.ok:
                print('Failed to download file {} {} - {}'.format(response.status_code, response.reason, file_))
                continue

            import ipdb; ipdb.set_trace()
            basedir = './{}'.format(os.path.dirname(__file__))
            filepath = './{}/{}'.format(os.path.dirname(__file__), os.path.basename(file_))
            os.mkdir(basedir)
            open(filepath, 'wb').write(response.content)



if __name__ == '__main__':
    usernames = get_user_names()
    user_files_all = {
        username: get_user_listing(username)
        for username in usernames
    }
    user_files = {
        username: files
        for username, files in user_files_all.items()
        if files
    }
    import ipdb; ipdb.set_trace()
