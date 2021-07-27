'''
bot_api 自定义功能的主要文件

主动命令格式：
@Resolutionmessage()
def bot_api(text):
    ...
    return res

中断命令格式：
@Resolutionmessage()
def bot_api(text):
    ...
    return (text[1],res,text[0])

@Resolutionmessage()
def i_bot_api(text):
    ...
    return ('',res)

自定义任务格式：
def bot_api():
    ...
    return res

ps: 如果注释带有 `key` 请填写key 否则不能直接使用,大多是聚合
'''

import requests
import os
import time
import random
import subprocess
from baiduspider import BaiduSpider
from dtanys import XDict
import base64
import json
from graia.application.message.elements.internal import Plain,Image,At,Face,Source,Voice


# 当前目录
onfile = os.path.split(__file__)[0]

# 权限控制 勿删
authority = {}

# 消息链解析
def Resolutionmessage(types = None):
    '''
    当 `types` 为消息类型时
    '''
    def wrapper(fun):
        def main(*args,**kwargs):
            if not types:
                return fun(args[0])
            else:
                return fun(args[0],args[1][types])
        return main
    return wrapper

## 自定义api

# 聚合天气 key
@Resolutionmessage()
def weather(city):
    data = {
        'city':city,
        'key':'',
    }
    url = "http://apis.juhe.cn/simpleWeather/query"
    r = requests.get(url, params=data)
    result = r.json()
    if result['error_code']==0:
        res = result['result']
        result = '城市' + ':' + res['city'] + '\n'
        for i,j in res['realtime'].items():
            result+=i + ':' + j + '\n'
    else:
        result = result['reason']

    return result

# 翻译
@Resolutionmessage()
def fanyiyoudao(string):
    data = {
        'doctype': 'json',
        'type': 'AUTO',
        'i': string
    }
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url, params=data)
    result = XDict(r.json(),'/*tgt').edict()
    return ''.join(result)

# 聚合IP地址 key
@Resolutionmessage()
def getIp(ips):
    data = {
        'ip':ips,
        'key':'',
    }
    url = "http://apis.juhe.cn/ip/ipNew"
    r = requests.get(url, params=data)
    result = r.json()
    if result['resultcode']=='200':
        res = result['result']
        result = ''
        for i,j in res.items():
            result+=i + ':' + j + '\n'
    else:
        result = result['reason']
    return result

# 图片
@Resolutionmessage()
def getImage(zhuti):
    url = 'https://source.unsplash.com/random/?' + zhuti.replace(' ','')
    res = requests.get(url)
    path = os.path.join(onfile,'getImage.png')
    with open(path,'wb') as f:
        f.write(res.content)
    return path

# 美图
@Resolutionmessage()
def meiImage(text):
    url = "https://cdn.seovx.com/ha/?mom=302"
    res = requests.get(url)
    path = os.path.join(onfile,'meiImage.png')
    with open(path,'wb') as f:
        f.write(res.content)
    return path

# 二维码 key
def erweiMa(text):
    data = {
        'text':text,
        'key':'',
        'type':2,
        'w':500,
    }
    url = "http://apis.juhe.cn/qrcode/api"
    res = requests.get(url, params=data)
    path = os.path.join(onfile,'erweiMa.png')
    with open(path,'wb') as f:
        f.write(res.content)
    return path

# 段子 key
@Resolutionmessage()
def duanZi(text):
    t = abs(int(time.time())-random.randint(10**6,10**9))
    print(t)
    data = {
        'sort':'desc',
        'key':'',
        'time':t,
        'page':random.randint(1,20),
        'pagesize':1,
    }
    url = "http://v.juhe.cn/joke/content/list.php"
    res = requests.get(url, params=data).json()
    if res['error_code']==0:
        res = res['result']['data'][0]['content']
    else:
        res = res['reason']
    return res

# 聊天
@Resolutionmessage()
def liaotian(text):
    url = "http://api.qingyunke.com/api.php"
    data = {
        'key':'free',
        'appid':0,
        'msg':text,
    }
    res = requests.get(url,params=data).json()
    res = res['content'].replace("{br}",'\n').replace('★','').split('\n')
    ress = ''
    for i in res:
        ress +=i.strip()+'\n'
    return ress.rstrip('\n').replace('菲菲','墨墨')

# 一言
@Resolutionmessage()
def oneYan(text):
    a1 = range(97,109)
    b1 = random.choice([chr(i) for i in a1])
    data = {
        'c':b1,
        'encode':'text',
        'charset':'utf-8',
        'max_length':100,
    }
    url = "https://v1.hitokoto.cn"
    res = requests.get(url, params=data)
    return res.text

# SSH
@Resolutionmessage()
def sshRun(text):
    msg = ''

    try:
        back = subprocess.Popen(text, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    except:
        msg = "shell 错误！"
    try:
        b0 = back[0].decode()
        b1 = back[1].decode()
    except UnicodeDecodeError:
        b0 = back[0].decode('gbk').strip()
        b1 = back[1].decode('gbk').strip()
    if b0:
        msg += b0
    elif b1:
        msg += b1
    return msg

# 百科
@Resolutionmessage()
def getBaike(text):
    spider = BaiduSpider()
    res = XDict(spider.search_baike(query=text),'/results//["des","title","url"]').edict()[0]
    return res[1] + '\n' + res[0] + '\n' + res[2].replace('https://baike.baidu.comhttp://baike.baidu.com','https://baike.baidu.com')

# 博客
@Resolutionmessage()
def getBlog(text):
    spider = BaiduSpider()

    res = spider.search_web(query=text, exclude=['news', 'video', 'tieba', 'baike','gitee','related','calc'])
    # pprint(res)
    try:
        res = '\n'.join(XDict(res,'/results[1]//["des","title","url"]').edict())
    except IndexError:
        res = '无搜索结果！'
    return res

# 帮助
@Resolutionmessage()
def get_help(text):
    res = '''墨墨机器人😄
    支持命令：
    翻译 >> 翻译 hello
    查询IP >> 查询IP 172.0.0.1
    天气 >> 天气北京
    图片 >> 图片natural(英文)
    段子 >> 段子
    一言 >> 一言
    识别 >> 识别(附带图片)
    识图 >> 识图(附带图片)
    百科 >> 百科华为
    博客 >> 博客luxncang
    美图 >> 美图
    音乐 >> 音乐青花瓷
    歌词 >> 歌词青花瓷
    runCode >> runCode(附带代码)
    '''
    return res

# 百度api key
APIKEY = ''
SECRETKEY = ''
def GetAccessToeken():
    token_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={ak}&client_secret={sk}'.format(ak=APIKEY, sk=SECRETKEY)
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    response = requests.post(url=token_host, headers=header)
    content = response.json()
    access_token = content.get("access_token")
    return access_token


'''
通用文字识别（高精度版）
'''
@Resolutionmessage(Image)
def ORCz(tuurl,message):
    url = [i.url for i in message]
    path = os.path.join(onfile,'识别图片.png')
    text = ''
    for i in url:
        res = requests.get(i)
        with open(path,'wb') as f:
            f.write(res.content)

        # 识别api url
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

        # 二进制方式打开图片文件
        with open(path, 'rb') as f:
            img = base64.b64encode(f.read())
        params = {"image":img}

        
        access_token = GetAccessToeken()
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            res = response.json()['words_result']      
            for i in res:
                text += i['words']+'\n\n'
    return text
    
'''
通用物体和场景识别
''' 
@Resolutionmessage(Image)
def shibie(tuurl,message):
    url = [i.url for i in message]
    path = os.path.join(onfile,'分析图片.png')
    text = ''
    res = requests.get(url[0])
    with open(path,'wb') as f:
        f.write(res.content)
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"

    # 二进制方式打开图片文件
    with open(path, 'rb') as f:
        img = base64.b64encode(f.read())

    params = {"image":img}
    access_token = GetAccessToeken()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    text = ''
    if response:
        for i in response.json()['result']:
            text+='置信度：'+str(i['score'])+'\n'
            text+='类别：'+i['root']+'\n'
            text+='结果：'+i['keyword']+'\n'
            try:
                text+='详情：'+i['baike_info']+'\n'
            except:
                pass
    if text=='\n':
        text+='无法识图！'
    return text

'''
人像动漫化
'''
@Resolutionmessage(Image)
def dongmanH(tuurl,message):
    url = [i.url for i in message]
    path = os.path.join(onfile,'漫画图片.png')
    res = requests.get(url[0])
    with open(path,'wb') as f:
        f.write(res.content)
    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime"
    # 二进制方式打开图片文件
    with open(path, 'rb') as f:
        img = base64.b64encode(f.read())
    params = {"image":img}
    access_token = GetAccessToeken()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        with open(path,'wb') as f:
            f.write(base64.b64decode(response.json()['image']))
    return path


# qq 音乐卡片
from playwright.sync_api import sync_playwright
import threading
def music_runs(playwright,text):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to https://y.qq.com/n/ryqq/search
    page.goto("https://y.qq.com/n/ryqq/search")
    # Click [placeholder="搜索音乐、MV、歌单、用户"]
    page.click("[placeholder=\"搜索音乐、MV、歌单、用户\"]")
    # Fill [placeholder="搜索音乐、MV、歌单、用户"]
    time.sleep(1)
    page.fill("[placeholder=\"搜索音乐、MV、歌单、用户\"]", text)
    # Click button:has-text("搜索")
    page.click("button:has-text(\"搜索\")")
    time.sleep(1)
    url = page.query_selector("#app > div.main > div > div > div.mod_songlist > ul.songlist__list > li:nth-child(1) > div > div.songlist__songname > span > a").get_attribute('href')

    page.goto(f"https://y.qq.com{url}")
    time.sleep(1)
    name = page.query_selector("#app > div > div.main > div.mod_data > div > div.data__name > h1").get_attribute('title')
    author = page.query_selector("#app > div > div.main > div.mod_data > div > div.data__singer").inner_text()
    img =  page.query_selector("#logo > img").get_attribute('src')
    lrc = page.query_selector("#lrc_content").inner_text()
    context.close()
    browser.close()
    return (name,f"https://y.qq.com{url}",f"https:{img}",author,lrc)

def qqmusic(text):
    with sync_playwright() as playwright:
        res = music_runs(playwright,text)
    return res

class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result   # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

def sendQqMusic(name,url,imgUrl,author,lrc):
    return f'''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="2" templateID="1" action="web" brief="[分享] {name}" sourceMsgId="0" url="{url}" flag="0" adverSign="0" multiMsgFlag="0"><item layout="2"><audio cover="{imgUrl}" src="nil" /><title>{name}</title><summary>{author}</summary></item><source name="QQ音乐" icon="https://i.gtimg.cn/open/app_icon/01/07/98/56/1101079856_100_m.png?date=20200503" action="app" a_actionData="com.tencent.qqmusic" /></msg>'''

# card
@Resolutionmessage()
def get_qqmusic(text):
    t = MyThread(qqmusic,args=(text,))
    t.start()
    t.join()
    res = t.get_result()
    return sendQqMusic(*res)

# 歌词
@Resolutionmessage()
def get_qqmusic_lrc(text):
    t = MyThread(qqmusic,args=(text,))
    t.start()
    t.join()
    res = t.get_result()
    return res[-1].replace('\n\n','\n')

Language = {
    'php5.3':15,
    'php5.4':16,
    'php5.5':3,
    'php5.6': 17,
    'php7':18,
    'php7.4':37,
    'python2.7':19,
    'python3':20,
    'C#':10,
    'F#':22,
    'java1.7':8,
    'java1.8':23,
    'shell':11,
    'C语言':7,
    'C++':7,
    'nasm':24,
    'go':6,
    'lua':25,
    'perl': 14,
    'ruby':1,
    'nodejs': 4,
    'Objective-C':12,
    'swift':21,
    'erlang':26,
    'rust': 27,
    'R语言':28,
    'scala':5,
    'haskell':29,
    'D语言':30,
    'clojure':2,
    'groovy':31,
    'lisp':32,
    'ocaml': 33,
    'CoffeeScript':35,
    'racket':35,
    'nim':36,
}

## 中断 api
# 触发模板 第一次触发命令 > 1_fun(text) > 第二次触发命令 > 2_fun(args)
'''
text ：tuple text[0]为当前命令 text[1]为替换掉当前命令的用户文本 
args ：tuple args[0]为当前命令 args[1]为替换掉当前命令的用户文本 args[2] 为第一次命令的text[1]
'''

# runCode
@Resolutionmessage()
def runCode_c(text):
    return (text[1]," 发送【语言类型】继续运行,如果有输入请以行换分隔！",'runCode')

@Resolutionmessage()
def getDai(args):
    print(args)
    language = args[0]
    stdin = '%0A'.join(args[1].strip('\n').split('\n'))
    if not stdin:
        stdin = None
    language = Language[language]
    code = args[2]
    print(language,stdin,code)
    code = str(base64.b64encode(code.encode("utf-8")), "utf-8")
    url = 'http://runcode-api2-ng.dooccn.com/compile2'
    headers = {'Host': 'runcode-api2-ng.dooccn.com', 'Connection': 'keep-alive', 'Content-Length': '210', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Origin': 'http://www.dooccn.com', 'Referer': 'http://www.dooccn.com/', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
    cookies = {'Set-CacheRemark': 'default'}
    data = {'language': language, 'code': code, 'stdin': stdin}
    res = requests.post(url, headers=headers,cookies=cookies, data=data).text
    print(res)
    res = json.loads(res)
    return ('',(res['output'] + res['errors']).rstrip('\n'))

# 授权
@Resolutionmessage()
def Authorize(text):
    return (text[1]," 发送【授权类别】继续运行！",'授权')

@Resolutionmessage()
def f_authorize(args):
    qqid = int(args[2].strip('\n').strip())
    if qqid in authority['member'][args[0]]:
        return ('',"有授权！")
    authority['member'][args[0]].append(qqid)
    with open(os.path.join(onfile,'授权',args[0]+'.txt'),'a',encoding='utf-8') as f:
        f.write(str(qqid) + '\n')
    return ('',"已授权！")

# OUT
@Resolutionmessage()
def out_auth(text):
    return (text[1]," 发送【OUT类别】继续运行！",'OUT')

@Resolutionmessage()
def f_out_auth(args):
    qqid = int(args[2].strip('\n').strip())
    if qqid in authority['member'][args[0]]:
        authority['member'][args[0]].remove(qqid)
        with open(os.path.join(onfile,'授权',args[0]+'.txt'),'w',encoding='utf-8') as f:
            for i in authority['member'][args[0]]:
                f.write(str(i) + '\n')
        return ('',f'{qqid} 已OUT！')
    else:
        return ('',f'{qqid} 无此类别授权！')

## 初始化api
def init_authority(auth):
    for i in auth['member']:
        try:
            with open(os.path.join(onfile,'授权',i+'.txt'),'r',encoding='utf-8') as f:
                auth['member'][i] += [int(i) for i in f if not i=='\n']
            auth['member'][i] = list(set(auth['member'][i]))
        except FileNotFoundError:
            pass

def run_silently(cmd: str) -> str:
    """返回系统命令的执行结果"""
    with os.popen(cmd) as fp:
        bf = fp._stream.buffer.read()
    try:
        return bf.decode().strip()
    except UnicodeDecodeError:
        return bf.decode('gbk').strip()

## 自定义任务

def hello_world():
    return 'hi'

# 早安
def zaoAn():
    url = "http://api.tianapi.com/txapi/zaoan/index"
    data = {
        'key':""
    }
    res = requests.get(url, params=data)
    return res.json()['newslist'][0]['content']