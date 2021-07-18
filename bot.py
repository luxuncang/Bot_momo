from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain,Image,At,Face,Source,Voice,PokeMethods
from graia.application.friend import Friend
from graia.application.group import Group, Member,MemberInfo
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter
from graia.application.event.messages import GroupMessage
from graia.application.entry import *
# bot_momo
from config import bot_session,interrupt_command,passive
from bot_tool import mfilter,ffilter,internal_mfilter,ffilter_mfilter,dict_slice,TimerTasks,Tasks

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(**bot_session)
)
inc = InterruptControl(bcc)

# Interrupt存储器
INTERRUPT = {i:{} for i in interrupt_command}

# 防撤回 存储器
WITHDRAWAL = {'group':{},'friend':{}}

# 侦测好友对话
@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend, message: MessageChain, source: Source):
    global WITHDRAWAL
    WITHDRAWAL['friend'][source.id] = message
    WITHDRAWAL['friend'] = dict_slice(WITHDRAWAL['friend'],-50)
    res = ffilter(message,friend)
    # print(source.time.timestamp())
    if res:
        im = await app.sendFriendMessage(friend, MessageChain.create(res['res']))
        # await  app.revokeMessage(im)
    else:
        res = ffilter_mfilter(message,friend)
        if res:
            m1 = res['args'][0]
            task1 = res['args'][2]
            await app.sendFriendMessage(friend, MessageChain.create(res['res']))
            @Waiter.create_using_function([FriendMessage])
            def waiters(
                event: FriendMessage,waiter_member: Friend, waiter_message: MessageChain
            ):  

                res = ffilter_mfilter(waiter_message,waiter_member,m1,command = interrupt_command[task1]['command'])
                if res:
                    INTERRUPT[task1][friend.id] = res['res']
                if all([
                    waiter_member.id == friend.id,
                    res
                ]):
                    return event
            await inc.wait(waiters)
            await app.sendFriendMessage(friend, MessageChain.create(INTERRUPT[task1][friend.id]))
    

# 侦测群对话
@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member, 
    source: Source
):  
    # print(message[Image][0].url)
    global WITHDRAWAL
    WITHDRAWAL['group'][source.id] = message
    WITHDRAWAL['group'] = dict_slice(WITHDRAWAL['group'],-50)
    # print(WITHDRAWAL)
    res = mfilter(message,member,group)
    if res:
        await app.sendGroupMessage(group, MessageChain.create(res['res']))
    else:
        res = internal_mfilter(message,member,group)
        if res:
            m1 = res['args'][0]
            task1 = res['args'][2]
            await app.sendGroupMessage(group, MessageChain.create(res['res']))
            @Waiter.create_using_function([GroupMessage])
            def waiter(
                event: GroupMessage, waiter_group: Group,
                waiter_member: Member, waiter_message: MessageChain
            ):  

                res = internal_mfilter(waiter_message,waiter_member,waiter_group,m1,interrupt_command = interrupt_command[task1]['command'])
                if res:
                    INTERRUPT[task1][member.id] = res['res']
                if all([
                    waiter_group.id == group.id,
                    waiter_member.id == member.id,
                    res
                ]):
                    return event
            await inc.wait(waiter)
            await app.sendGroupMessage(group, MessageChain.create(INTERRUPT[task1][member.id]))

# 监听群撤回事件
@bcc.receiver("GroupRecallEvent")
async def function_GroupRecallEvent(event:GroupRecallEvent):
    if passive['防撤回']['status']:
        if passive['防撤回']['callback'] == 'friend':
            # await app.sendGroupMessage(passive['防撤回']['id'],)
            await app.sendFriendMessage(passive['防撤回']['id'], MessageChain.join(MessageChain.create([Plain('撤回消息\n----------\n')]),MessageChain.asSendable(WITHDRAWAL['group'][event.messageId])))
        elif passive['防撤回']['callback'] == 'group':
            await app.sendGroupMessage(passive['防撤回']['id'], MessageChain.asSendable(WITHDRAWAL['group'][event.messageId]))

# 监听好友撤回事件
@bcc.receiver("FriendRecallEvent")
async def function_GroupRecallEvent(event:FriendRecallEvent):
    if passive['防撤回']['status']:
        if passive['防撤回']['callback'] == 'friend':
            await app.sendFriendMessage(passive['防撤回']['id'], MessageChain.asSendable(WITHDRAWAL['friend'][event.messageId]))
        elif passive['防撤回']['callback'] == 'group':
            await app.sendGroupMessage(passive['防撤回']['id'], MessageChain.asSendable(WITHDRAWAL['friend'][event.messageId]))

# 定时任务
TimerTasks(Tasks)

app.launch_blocking()


