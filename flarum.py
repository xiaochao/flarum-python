#coding=utf-8

import requests
import simplejson as json

class Flarum(object):
    def __init__(self, url=None, timeout=3):
        if not url:
            self.base_url = 'http://1juh.com/'
        else:
            self.base_url = url
        self.timeout = timeout
        self.token = None
        self.headers = {'Origin': 'http://1juh.com', 'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6',
                        'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36'
                                      ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                        'Connection': 'keep-alive',
                        'Cookie': 'flarum_remember=xKclcR8isXyikPnYvJpSzeaqFpPnCtJVzLySJYyc;'
                                  ' PHPSESSID=sok1curhdl9daghgbt1uuug3g4', 'Pragma': 'no-cache',
                        'Cache-Control': 'no-cache', 'Referer': 'http://1juh.com/',
                        'Content-Type': 'application/json; charset=UTF-8',
                        'Authorization': 'Token '}

    def http_requests(self, url, params, method='post'):
        try:
            if url.find('/api/token') > 0:
                headers = dict()
            else:
                headers = self.headers
            if method == 'post':
                r = requests.post(url, data=params, timeout=self.timeout, headers=headers)
            else:
                r = requests.get(url, params=params, timeout=self.timeout, headers=headers)
            if r.status_code != 200:
                print 'http code error:', r.status_code
                return None
            return json.loads(r.text)
        except Exception, e:
            print e
            return None

    def get_token(self, username, password):
        url = self.base_url+'/api/token'
        params = {'identification': username, 'password': password}
        data = self.http_requests(url, params)
        if not data:
            return False
        self.token = data.get('token')
        if not self.token:
            return False
        self.headers['Authorization'] = 'Token '+self.token
        return True

    def get_discussions(self):
        url = self.base_url+'/api/discussions'
        data = self.http_requests(url, {}, method='get')
        print json.dumps(data)

    def create_discussions(self, title, description):
        url = self.base_url+'/api/discussions'
        params = {"data":
                      {
                          "type": "discussions",
                          "attributes":{
                              "title": title,
                              "content": description
                          },
                          "relationships":{
                              "tags":{
                                  "data":[{
                                      "type":"tags","id":"1"
                                  }]
                              }
                          }
                      }
                  }
        data = self.http_requests(url, json.dumps(params))
        print data

    def get_post(self):
        pass

if __name__ == '__main__':
    import sys
    test = Flarum()
    is_token = test.get_token(sys.argv[1], sys.argv[2])
    test.create_discussions('测试登录成功后是否能够成功', '测试使用api登录成功后能否创建')
