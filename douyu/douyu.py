# 获取斗鱼直播间的真实流媒体地址，默认最高画质
# 使用 https://github.com/wbt5/real-url/issues/185 中两位大佬@wjxgzz @4bbu6j5885o3gpv6ss8找到的的CDN，在此感谢！
import hashlib
import re
import time

from quickjs import Function
import requests


class DouYu:
    """
    可用来替换返回链接中的主机部分
    两个阿里的CDN：
    dyscdnali1.douyucdn.cn
    dyscdnali3.douyucdn.cn
    墙外不用带尾巴的akm cdn：
    hls3-akm.douyucdn.cn
    hlsa-akm.douyucdn.cn
    hls1a-akm.douyucdn.cn
    """

    def __init__(self, rid):
        """
        房间号通常为1~8位纯数字，浏览器地址栏中看到的房间号不一定是真实rid.
        Args:
            rid:
        """
        self.did = '10000000000000000000000000001501'
        self.t10 = str(int(time.time()))
        self.t13 = str(int((time.time() * 1000)))

        self.s = requests.Session()
        self.res = self.s.get('https://m.douyu.com/' + str(rid)).text
        result = re.search(r'rid":(\d{1,8}),"vipId', self.res)

        if result:
            self.rid = result.group(1)
        else:
            raise Exception('房间号错误')

    @staticmethod
    def md5(data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def get_pre(self):
        url = 'https://playweb.douyucdn.cn/lapi/live/hlsH5Preview/' + self.rid
        data = {
            'rid': self.rid,
            'did': self.did
        }
        auth = DouYu.md5(self.rid + self.t13)
        headers = {
            'rid': self.rid,
            'time': self.t13,
            'auth': auth
        }
        res = self.s.post(url, headers=headers, data=data).json()
        error = res['error']
        data = res['data']
        key = ''
        if data:
            rtmp_live = data['rtmp_live']
            rtmp_url = data['rtmp_url']
        return rtmp_url + '/' + rtmp_live

    def get_js(self):
        result = re.search(r'(function ub98484234.*)\s(var.*)', self.res).group()
        func_ub9 = re.sub(r'eval.*;}', 'strc;}', result)
        f = Function("ub98484234", func_ub9)
        res = f()


        v = re.search(r'v=(\d+)', res).group(1)
        rb = DouYu.md5(self.rid + self.did + self.t10 + v)

        func_sign = re.sub(r'return rt;}\);?', 'return rt;}', res)
        func_sign = func_sign.replace('(function (', 'function sign(')
        func_sign = func_sign.replace('CryptoJS.MD5(cb).toString()', '"' + rb + '"')

        f = Function('sign', func_sign)
        params = f(self.rid, self.did, self.t10)
        params += '&ver=219032101&rid={}&rate=0'.format(self.rid)

        url = 'https://m.douyu.com/api/room/ratestream'

        res = self.s.post(url, params=params).text
        key = re.search(r'(\d{1,8}[0-9a-zA-Z]+)_?\d{0,4}(.m3u8|/playlist)', res).group(1)

        return key

    def get_real_url(self):
        error, key = self.get_pre()
        if error == 0:
            pass
        elif error == 102:
            raise Exception('房间不存在')
        elif error == 104:
            raise Exception('房间未开播')
        else:
            key = self.get_js()
        real_url = {}
        real_url["flv"] =    "http://akm-tct.douyucdn.cn/live/{}.flv?uuid=".format(key)
        real_url["x-p2p"] =  "http://ws-tct.douyucdn.cn/live/{}.flv?uuid=".format(key)
        return real_url

if __name__ == '__main__':
    r = input('输入斗鱼直播间号：\n')
    s = DouYu(r)
    print(s.get_pre())
