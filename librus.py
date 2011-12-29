# 2011.12.29 09:08:48 CET
import urllib
import httplib
import re
import os

import librus_parser

login_data = open(os.path.join(os.path.expanduser('~'), '.librus_login')).read().strip().split(':',1)
login_data = {'login': login_data[0], 'passwd': login_data[1]}

class LibrusError(Exception):
    pass

def fetch(url, headers = {}, **data):
    headers = dict(headers)
    headers.update({'User-Agent': 'GradesBot/1.0 (+http://zielm.com/librusbot)'})
    if data:
        post_data = urllib.urlencode(data)
    else:
        post_data = None
    conn = httplib.HTTPSConnection('dziennik.librus.pl')
    #conn.set_debuglevel(2)
    conn.request('GET' if not post_data else 'POST', url, post_data, headers)
    resp = conn.getresponse()
    
    set_cookie = resp.getheader('set-cookie')
    if set_cookie:
        global php_sid
        php_sid = re.match('PHPSESSID=(.+?)(,|;)', set_cookie).group(1)
    
    return resp

def init_session():
    global php_sid
    resp = fetch('/mobile/index')

def login(login=login_data['login'], password=login_data['passwd']):
    resp = fetch('/mobile/index',
                 headers={'Cookie': 'TestCookie=1; PHPSESSID=' + php_sid,
                          'Content-type': 'application/x-www-form-urlencoded'},
                 login=login, passwd=password, loguj='loguj')
    if resp.getheader('location') != '/mobile/uczen_index':
        raise LibrusError('Failed to login')

def get_marks():
    resp = fetch('/mobile/oceny', headers={'Cookie': 'TestCookie=1; PHPSESSID=' + php_sid})
    data = resp.read()
    return librus_parser.get_marks(data)

if __name__ == '__main__':
    init_session()
    login()
    print get_marks()
