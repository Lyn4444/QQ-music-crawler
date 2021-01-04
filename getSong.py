'''
@Author: your name
@Date: 2020-07-29 20:27:01
LastEditTime: 2020-08-23 22:34:53
LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \qqmuusic\getSong.py
'''


import execjs,requests
from urllib import parse


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Referer':'https://y.qq.com/n/yqq/singer/003ya8w823iLae.html',
}


def getSign(data):
    with open('./jsdecoding.js', 'r', encoding='utf-8') as f:
        js_content = f.read()

    js_exec = execjs.compile(js_content)
    sign = js_exec.call('getSecuritySign',data)
    return sign


def download():
    data = '{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"8254175482","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"8254175482","songmid":["000wY3Pq3uZ0TK"],"songtype":[0],"uin":"3077002706","loginflag":1,"platform":"20"}},"comm":{"uin":3077002706,"format":"json","ct":24,"cv":0}}'
    sign = getSign(data)   
    qq = '' 
    # getplaysongvkey7287781479612441替换成对应的
    url = 'https://u.y.qq.com/cgi-bin/musics.fcg?-=getplaysongvkey7287781479612441'\
        '&g_tk=1291538537&sign={}&loginUin={}'\
        '&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0'\
        '&platform=yqq.json&needNewCode=0&data={}'.format(sign,qq,parse.quote(data))
    html = requests.get(url,headers = headers).json()
    try:
        purl = html['req_0']['data']['midurlinfo'][0]['purl']
        filename = html['req_0']['data']['midurlinfo'][0]['filename']
        url = 'http://119.147.228.27/amobile.music.tc.qq.com/{}'.format(purl)
        html = requests.get(url,headers = headers)
        html.encoding = 'utf-8'
        with open(filename,'wb') as f:
            f.write(html.content)   
            print('succeed')
    except:
        print('failed')


if __name__ == '__main__':
    download()

