from graia.application.message.elements.internal import Plain,Image,At,Face,Source,Voice
from config import authority,command,interrupt_command,bot_session,passive
# 命令过滤

# 查询指令头
def getComandHead(act,men):
    return act in [zid.target for zid in men]

# 查询指令体
def getComandBody(com,men):
    men = [i.text for i in men]
    for i in com:
        for j in men:
            if i in j:
                return (i,j.replace(i,''))
    return False

# 查询授权的群范围
def getGroups(gid):
    for i,j in authority['group'].items():
        if gid in j:
            return i
    return False

# 查看授权的人    
def getMembers(mid):
    if mid in authority['shield']:
        return False
    for i,j in authority['member'].items():
        if mid in j:
            return i
    return False

# 构造消息链
def structure(mode,text):
    res = None
    if mode==Plain:
        res = Plain(text)
    elif mode==Image:
        res = Image.fromLocalFile(text)
    elif mode==At:
        res = At(text)
    else:
        assert False,'Exhibition five this type!'
    return res

# 功能调用
def function_call(method,mode,isAt,mid,*args):
    res = {'res':[]}
    huitiao = method(*args)
    if isAt:
        res['res'].append(At(mid))
        res['res'].append(Plain('\n'))
    if mode==Plain:
        res['res'].append(structure(mode,huitiao))
    elif mode==Image:
        res['res'].append(structure(mode,huitiao))
    elif isinstance(mode,list):
        for i,j in enumerate(mode):
                res['res'].append(structure(j,huitiao[i]))
    else:
        assert False,'Exhibition five this type!'
    return res

# 功能调用
def function_call_internal(method,mode,isAt,mid,*args):
    res = {'res':[],'args':[]}
    huitiao = method(*args)
    if isAt:
        res['res'].append(At(mid))
        res['res'].append(Plain('\n'))
    if mode==Plain:
        res['res'].append(structure(mode,huitiao[1]))
    elif mode==Image:
        res['res'].append(structure(mode,huitiao[1]))
    elif isinstance(mode,list):
        for i in enumerate(mode):
                res['res'].append(structure(mode[i],huitiao[1][i]))
    else:
        assert False,'Exhibition five this type!'
    res['args'] = huitiao
    return res

# 群会话消息过滤器
def mfilter(message,member,group,*args):
    qc = getGroups(group.id)
    if qc: # 过滤群
        cm = getComandBody(command,message[Plain])
        if cm and cm[0] in command: # 过滤命令
            qm = getMembers(member.id)
            if qm and (qm=='all' or (cm[0] in authority['authlist'][qm])): # 过滤用户权限
                if command[cm[0]]['trigger']:
                    return function_call(command[cm[0]]['method'],command[cm[0]]['mode'],command[cm[0]]['isAt'],member.id,(cm[1],*args),message)
                else:
                    if getComandHead(bot_session['account'],message[At]):
                        return function_call(command[cm[0]]['method'],command[cm[0]]['mode'],command[cm[0]]['isAt'],member.id,(cm[1],*args),message)
    cm = getComandBody(interrupt_command,message[Plain])
    if qc and getComandHead(bot_session['account'],message[At]) and cm and (not cm[0] in interrupt_command):
        return function_call(command['/chat']['method'],command['/chat']['mode'],command['/chat']['isAt'],member.id,message[Plain],message)
    return False

# 中断群会话消息过滤器
def internal_mfilter(message,member,group,*args,interrupt_command=interrupt_command):
    qc = getGroups(group.id)
    if qc: # 过滤群
        cm = getComandBody(interrupt_command,message[Plain])
        if cm and cm[0] in interrupt_command: # 过滤命令
            qm = getMembers(member.id)
            if qm and (qm=='all' or (cm[0] in authority['authlist'][qm])): # 过滤用户权限
                if interrupt_command[cm[0]]['trigger']:
                    return function_call_internal(interrupt_command[cm[0]]['method'],interrupt_command[cm[0]]['mode'],interrupt_command[cm[0]]['isAt'],member.id,(*cm,*args),message)
                else:
                    if getComandHead(bot_session['account'],message[At]):
                        return function_call_internal(interrupt_command[cm[0]]['method'],interrupt_command[cm[0]]['mode'],interrupt_command[cm[0]]['isAt'],member.id,(*cm,*args),message)
    if getComandHead(bot_session['account'],message[At]):
        return function_call(command['/chat']['method'],command['/chat']['mode'],command['/chat']['isAt'],member.id,message[Plain],message)
    return False

# 好友会话消息过滤器
def ffilter(message,member):
    cm = getComandBody(command,message[Plain])
    if cm and cm[0] in command: # 过滤命令
        qm = getMembers(member.id)
        if qm and (qm=='all' or (cm[0] in authority['authlist'][qm])): # 过滤用户权限
            return function_call(command[cm[0]]['method'],command[cm[0]]['mode'],False,member.id,cm[1],message)
    if cm and (not cm[0] in interrupt_command):
        return function_call(command['/chat']['method'],command['/chat']['mode'],False,member.id,message[Plain],message)
    return False

# 中断好友会话消息过滤器
def ffilter_mfilter(message,member,*args,command = interrupt_command):
    cm = getComandBody(command,message[Plain])
    if cm and cm[0] in command: # 过滤命令
        qm = getMembers(member.id)
        if qm and (qm=='all' or (cm[0] in authority['authlist'][qm])): # 过滤用户权限
           return function_call_internal(command[cm[0]]['method'],command[cm[0]]['mode'],False,member.id,(*cm,*args),message)
    if cm:
        return function_call(command['/chat']['method'],command['/chat']['mode'],False,member.id,message[Plain],message)
    return False


# clear cache
def clear_cache(cache,mid,message):
    cache[mid] = message
    if len(cache) > 50:
        cache = cache[-50:]
    return cache

# 字典切片
def dict_slice(adict, start, end=None):
    keys = adict.keys()
    dict_slice = {}
    for k in list(keys)[start:end]:
        dict_slice[k] = adict[k]
    return dict_slice


## 自定义api工具
import requests
host = bot_session['host'] + '/'
account = bot_session['account']
sessionKey = ''


# 获取sessionKey
def getSession():
    global sessionKey
    url = host + 'auth'
    headers = {'Content-Type': 'application/json'}
    data = {
        "authKey": bot_session["authKey"]
    }
    res = requests.post(url=url, headers=headers,json=data)
    sessionKey = res.json()["session"]
    return res.json()

# 激活会话
def verify():
    url = host + 'verify'
    headers = {'Content-Type': 'application/json'}
    data = {
        "sessionKey": sessionKey,
        "qq": account
    }
    res = requests.post(url=url, headers=headers,json=data)
    return res.json()

# 控制台
def conRun():
    getSession()
    verify()

# 群消息
def sendGroupMessage(group,text):
    conRun()
    url = host + 'sendGroupMessage'
    headers = {'Content-Type': 'application/json'}
    data = {
        "sessionKey": sessionKey,
        "target": group,
        "messageChain": [
        { "type": "Plain", "text": text },
    ]
    }
    res = requests.post(url=url, headers=headers,json=data)
    return res.json() 

# 好友消息
def sendFriendMessage(target,text):
    conRun()
    url = host + 'sendFriendMessage'
    headers = {'Content-Type': 'application/json'}
    data = {
        "sessionKey": sessionKey,
        "target": target,
        "messageChain": [
        { "type": "Plain", "text": text },
    ]
    }
    res = requests.post(url=url, headers=headers,json=data)
    return res.json() 


## 定时任务

# Timing task
import datetime
from threading import Timer

# 计时器
def next_cycle(tast_time):
    now_time = datetime.datetime.now()
    # 获取明天时间
    next_time = now_time + datetime.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
    # 获取明天任务点时间
    next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day) + f" {tast_time}", "%Y-%m-%d %H:%M:%S")
    # # 获取昨天时间

    # 获取距离明天任务点时间，单位为秒
    timer_start_time = (next_time - now_time).total_seconds()
    print(int(timer_start_time))

class TimingTask:

    def __init__(self,method,cycle,callback,id):
        self.method = method
        self.callback = callback
        self.id = id
        self.cycle = cycle
        self.wait = cycle
        if callback == 'friend':
            self.send = sendFriendMessage
        elif callback == 'group':
            self.send = sendGroupMessage
        else:
            assert False, 'Please use the correct callback type!'

    def task(self):
        self.send(self.id,self.method())
        # print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        if isinstance(self.wait,int):
            self.cycle = self.cycle
        elif isinstance(self.wait,str):
            self.cycle = next_cycle(self.wait)
        t = Timer(self.cycle,self.task)
        t.start()

Tasks = [TimingTask(i['method'],i['cycle'],i['callback'],i['id']) for i in passive['定时任务'] if i['status']]

def TimerTasks(tasts):
    for i in tasts:
        i.task()

# TimerTasks(Tasks)