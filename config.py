'''
bot_momo 配置文档
'''
from graia.application.message.elements.internal import Plain, Image, At, Face, Source, Voice, Xml
from bot_api import weather, fanyiyoudao, getIp, getImage, erweiMa, duanZi, liaotian, sshRun, meiImage, oneYan, getBaike, getBlog, get_qqmusic, get_qqmusic_lrc, runCode_c, Language, getDai, Authorize, f_authorize, out_auth, f_out_auth, hello_world, ORCz, shibie, dongmanH, zaoAn
import bot_api

## 机器人配置
bot_session = {
    'host': "http://127.0.0.1:8000",
    'authKey': "", # 填入 authKey
    'account': 1000000, # 你的机器人的 qq 号
    'websocket': True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
}

## 权限配置(机器人响应的范围) 默认根据类别划分,可添加自定义类别,member优先级高于group,即只要member有权限就可触发命令，无论group是否有权限
bot_api.authority = {
    'group':{
        'all':[],
        'base':[],
    },
    'member':{
        'all':[],
        'base':[],
    },
    'shield':[], # 屏蔽对象qq

    'authlist':{
        'base':[]
    } # 填写 `command`
}

# 持久化权限
authority = bot_api.authority
bot_api.init_authority(bot_api.authority)


## 功能配置

# 被动命令
'''
status : bool 是否启用该功能
method : 任务函数
callback : str 返回类型(friend,group)
id : int 群id或好友id
cycle : int or dict 定时任务周期(秒) 如果为dict则是明天定时任务 
'''
passive = {
    '防撤回': {'status': True, 'callback': 'friend', 'id': 1},
    '定时任务':[
        {'status': True, 'method': hello_world, 'cycle' : 10,'callback': 'friend', 'id': 1},
        {'status': True, 'method': zaoAn, 'cycle' : '08:30:00','callback': 'friend', 'id': 1},
    ]
}

# 主动命令
'''
command[key] : str 为触发命令
method : function 功能函数
trigger : bool 触发扳机 为True时 不用@机器人
mode ：消息类型 当为迭代对象时,method也要返回对应消息类型的迭代对象
isAt ：bool 回调是否@
command[command] : 命令链
'''

command = {
    '天气': {'method': weather, 'trigger': True, 'mode': Plain, 'isAt': True},
    '翻译': {'method': fanyiyoudao,'trigger': True, 'mode': Plain, 'isAt': True},
    '查询IP': {'method': getIp,'trigger': True, 'mode': Plain, 'isAt': True},
    '图片': {'method': getImage,'trigger': True, 'mode': Image, 'isAt': True},
    '美图': {'method': meiImage,'trigger': True, 'mode': Image, 'isAt': True},
    '二维码': {'method': erweiMa,'trigger': True, 'mode': Image, 'isAt': False},
    '段子': {'method': duanZi,'trigger': True, 'mode': Plain, 'isAt': False},
    '一言': {'method': oneYan,'trigger': True, 'mode': Plain, 'isAt': False},
    'SSH': {'method': sshRun,'trigger': True, 'mode': Plain, 'isAt': False},
    '百科': {'method': getBaike,'trigger': True, 'mode': Plain, 'isAt': False},
    '博客': {'method': getBlog,'trigger': True, 'mode': Plain, 'isAt': False},
    '音乐': {'method': get_qqmusic,'trigger': True, 'mode': Xml, 'isAt': False},
    '歌词': {'method': get_qqmusic_lrc,'trigger': True, 'mode': Plain, 'isAt': False},
    '识别': {'method': ORCz,'trigger': True, 'mode': Plain, 'isAt': False},
    '识图': {'method': shibie,'trigger': True, 'mode': Plain, 'isAt': False},
    '头像': {'method': dongmanH,'trigger': True, 'mode': Image, 'isAt': False},
    '/chat': {'method': liaotian,'trigger': False, 'mode': Plain, 'isAt': False},
    '帮助' : {'method': liaotian,'trigger': False, 'mode': Plain, 'isAt': False}
}

# 中断命令

interrupt_command = {
    'runCode': {'method': runCode_c, 'trigger': True, 'mode': Plain, 'isAt': True, 'command':{i:{'method': getDai,'trigger': True, 'mode': Plain, 'isAt': True} for i in Language}},
    '授权': {'method': Authorize, 'trigger': False, 'mode': Plain, 'isAt': True, 'command': {i:{'method': f_authorize,'trigger': True, 'mode': Plain, 'isAt': True} for i in authority['member']}},
    'OUT': {'method': out_auth, 'trigger': False, 'mode': Plain, 'isAt': True, 'command': {i:{'method': f_out_auth,'trigger': True, 'mode': Plain, 'isAt': True} for i in authority['member']}}
}

