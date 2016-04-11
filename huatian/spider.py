# -*- coding=utf8 -*-
from urllib import urlencode
from requests import Session
from extension import mongo_collection

session = Session()
LOGIN_HEADERS = {
    'Host': 'reg.163.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/webp,*/*;q=0.8',
    'Origin': 'http://love.163.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/49.0.2623.110 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://love.163.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Cookie': '_ntes_nnid=d53195032b58604628528cd6a374d63f,1460206631682; '
              '_ntes_nuid=d53195032b58604628528cd6a374d63f',
}
SEARCH_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'love.163.com',
    'Origin': 'http://love.163.com',
    'Pragma': 'no-cache',
    'Referer': 'http://love.163.com/search/user',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/49.0.2623.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def login():
    """登陆花田"""
    data = {
        'username':'xxxxxx',
        'password':'xxxxxx',
        'url':'http://love.163.com/?checkUser=1&vendor=love.pLogin',
        'product':'ht',
        'type':'1',
        'append':'1',
        'savelogin':'1',
    }
    response = session.post('https://reg.163.com/logins.jsp',
                            headers=LOGIN_HEADERS, data=urlencode(data))
    assert response.ok


def search():
    """按照上海各个区和年龄段进行搜索"""
    for city in xrange(1, 20):
        for age in xrange(22, 27, 2):
            data = {
                'province': '2',
                'city': str(city),
                'age': '{}-{}'.format(age, age + 1),
                'condition': '1',
            }
            response = session.post('http://love.163.com/search/user/list',
                                    headers=SEARCH_HEADERS, data=urlencode(data))
            if not response.ok:
                print 'city:{} age:{} failed'.format(city, age)
                continue

            users = response.json()['list']
            for user in users:
                mongo_collection.update({'id': user['id']}, user, upsert=True)

if __name__ == '__main__':
    login()
    search()
