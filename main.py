#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import SeatKiller
import warnings
import getpass
import datetime
import time
import re
import sys

warnings.filterwarnings('ignore')
token = '75PLJJO8PV12084027'  # 预先移动端抓包获取
running = True

username = input('请输入学号：')
password = getpass.getpass('请输入图书馆密码：')

SK = SeatKiller.SeatKiller(token, username, password)

if SK.GetToken():
    SK.GetUsrInf()
    id = SK.CheckResInf()
    if id:
        if input('\n是否取消此预约信息（1.是 2.否）：') == '1':
            if not SK.CancelReservation(id):
                print('\n取消预约失败，请稍等后重试')
                sys.exit()
else:
    print('\n登陆失败，请稍等后重试')
    sys.exit()

mode = input('\n请选择信息输入模式（1.自动 2.手动 3.手动指定时间）：')
if mode == '1':
    buildingId = '1'
    roomId = '0'
    seatId = '7469'
    startTime = '480'
    endTime = '1320'
    rooms = SK.xt
    exchange = True
    SK.to_addr = '879316283@qq.com'
    if input('\n是否进入捡漏模式（1.是 2.否）：') == '1':
        response = SK.Loop(buildingId, rooms, startTime, endTime)
        if response[0] in map(str, range(10)) and exchange:
            SK.ExchangeLoop(buildingId, startTime, endTime, response)
        sys.exit()
elif mode == '2':
    buildingId = input('请输入分馆编号（1.信息科学分馆 2.工学分馆 3.医学分馆 4.总馆）：')
    if buildingId == '1':
        rooms = SK.xt
        if input('若抢到的座位位于\'一楼3C创客空间\'，是否尝试换座（1.是 2.否）：') == '1':
            exchange = True
        else:
            exchange = False
    elif buildingId == '2':
        rooms = SK.gt
        exchange = False
    elif buildingId == '3':
        rooms = SK.yt
        exchange = False
    elif buildingId == '4':
        rooms = SK.zt
        exchange = False
    else:
        print('分馆编号输入不合法，已默认设置为\'信息科学分馆\'')
        buildingId = '1'
        rooms = SK.xt
        if input('若抢到的座位位于\'一楼3C创客空间\'，是否尝试换座（1.是 2.否）：') == '1':
            exchange = True
        else:
            exchange = False

    startTime = input('请输入开始时间（以分钟为单位，从0点开始计算）：')
    endTime = input('请输入结束时间（以分钟为单位，从0点开始计算）：')

    SK.to_addr = input('请输入邮箱地址，抢座成功之后将发送邮件提醒（若不需要邮件提醒，此项可放空）：')
    mail_addr = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    if mail_addr == '':
        print('未输入邮箱地址，无法发送邮件提醒')
        SK.to_addr = False
    elif re.match(mail_addr, SK.to_addr):
        print('邮箱地址正确，可以发送邮件提醒')
    else:
        print('邮箱地址有误，无法发送邮件提醒')
        SK.to_addr = False

    if input('是否进入捡漏模式（1.是 2.否）：') == '1':
        response = SK.Loop(buildingId, rooms, startTime, endTime)
        if response[0] in map(str, range(10)) and exchange:
            SK.ExchangeLoop(buildingId, startTime, endTime, response)
        sys.exit()
    else:
        if buildingId == '1':
            roomId = input('已获取区域列表：4.一楼3C创客空间\n'
                           '             5.一楼创新学习讨论区\n'
                           '             6.二楼西自然科学图书借阅区\n'
                           '             7.二楼东自然科学图书借阅区\n'
                           '             8.三楼西社会科学图书借阅区\n'
                           '             9.四楼西图书阅览区\n'
                           '             10.三楼东社会科学图书借阅区\n'
                           '             11.四楼东图书阅览区\n'
                           '             12.三楼自主学习区\n'
                           '             14.3C创客-双屏电脑（20台）\n'
                           '             15.创新学习-MAC电脑（12台）\n'
                           '             16.创新学习-云桌面（42台）\n'
                           '请输入房间编号（若由系统自动选择请输入\'0\'）：')
        elif buildingId == '2':
            roomId = input('已获取区域列表：19.201室-东部自科图书借阅区\n'
                           '             29.2楼-中部走廊\n'
                           '             31.205室-中部电子阅览室笔记本区\n'
                           '             32.301室-东部自科图书借阅区\n'
                           '             33.305室-中部自科图书借阅区\n'
                           '             34.401室-东部自科图书借阅区\n'
                           '             35.405室中部期刊阅览区\n'
                           '             37.501室-东部外文图书借阅区\n'
                           '             38.505室-中部自科图书借阅区\n'
                           '请输入区域编号（若由系统自动选择请输入\'0\'）：')
        elif buildingId == '3':
            roomId = input('已获取区域列表：20.204教学参考书借阅区\n'
                           '             21.302中文科技图书借阅B区\n'
                           '             23.305科技期刊阅览区\n'
                           '             24.402中文文科图书借阅区\n'
                           '             26.502外文图书借阅区\n'
                           '             27.506医学人文阅览区\n'
                           '请输入房间编号（若由系统自动选择请输入\'0\'）：')
        else:
            roomId = input('已获取区域列表：39.A1-座位区\n'
                           '             40.C1自习区\n'
                           '             51.A2\n'
                           '             52.A3\n'
                           '             56.B3\n'
                           '             59.B2\n'
                           '             60.A4\n'
                           '             61.A5\n'
                           '             62.A1-沙发区\n'
                           '             65.B1\n'
                           '             66.A1-苹果区\n'
                           '请输入房间编号（若由系统自动选择请输入\'0\'）：')

        if roomId == '0':
            seatId = '0'
        else:
            seatId = input('请输入座位ID（若由系统自动选择请输入\'0\'）：')
else:
    buildingId = '1'
    roomId = '0'
    seatId = '7469'
    rooms = SK.xt
    exchange = True
    SK.to_addr = '879316283@qq.com'
    startTime = input('请输入开始时间（以分钟为单位，从0点开始计算）：')
    endTime = input('请输入结束时间（以分钟为单位，从0点开始计算）：')
    if input('是否进入捡漏模式（1.是 2.否）：') == '1':
        response = SK.Loop(buildingId, rooms, startTime, endTime)
        if response[0] in map(str, range(10)) and exchange:
            SK.ExchangeLoop(buildingId, startTime, endTime, response)
        sys.exit()

while running:
    if datetime.datetime.now() < datetime.datetime.replace(datetime.datetime.now(), hour=22, minute=14, second=40):
        print('\n------------------------准备获取token------------------------')
        SK.Wait(22, 14, 40)
    else:
        print('\n------------------------开始获取token------------------------')
    try_booking = True
    date = datetime.date.today() + datetime.timedelta(days=1)
    date = date.strftime('%Y-%m-%d')
    print('\ndate:' + date)

    if SK.GetToken():
        SK.GetBuildings()
        SK.GetRooms(buildingId)
        if roomId != '0':
            SK.GetSeats(roomId, date)

        if datetime.datetime.now() < datetime.datetime.replace(datetime.datetime.now(), hour=22, minute=15, second=0):
            SK.Wait(22, 15, 0)
        elif datetime.datetime.now() > datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=45,
                                                                 second=0) and exchange:
            print('\n预约系统开放时间已过，准备进入捡漏模式')
            SK.Wait(0, 59, 59, nextDay=True)
            response = SK.Loop(buildingId, rooms, startTime, endTime)
            if response[0] in map(str, range(10)) and exchange:
                SK.ExchangeLoop(buildingId, startTime, endTime, response)
            sys.exit()
        print('\n------------------------开始预约次日座位------------------------')
        while try_booking:
            if seatId != '0':
                if SK.BookSeat(seatId, date, startTime, endTime)[0] in map(str, range(10)):
                    try_booking = False
                else:
                    print('\n指定座位预约失败，尝试检索其他空位...')
                    seatId = '0'
            elif datetime.datetime.now() < datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=45,
                                                                     second=0):
                SK.freeSeats = []
                if roomId == '0':
                    for i in rooms:
                        if SK.SearchFreeSeat(buildingId, i, date, startTime, endTime) == 'Connection lost':
                            print('\n连接丢失，30秒后尝试继续检索空位')
                            time.sleep(30)
                else:
                    print('\n尝试检索同区域其他座位...')
                    if SK.SearchFreeSeat(buildingId, roomId, date, startTime, endTime) != 'Success':
                        print('\n当前区域暂无空位，尝试全馆检索空位...')
                        for i in rooms:
                            if SK.SearchFreeSeat(buildingId, i, date, startTime, endTime) == 'Connection lost':
                                print('\n连接丢失，30秒后尝试继续检索空位')
                                time.sleep(30)

                for freeSeatId in SK.freeSeats:
                    response = SK.BookSeat(freeSeatId, date, startTime, endTime)
                    if response == 'Success':
                        try_booking = False
                        break
                    elif response[0] in map(str, range(10)) and exchange:
                        try_booking = False
                        SK.ExchangeLoop(buildingId, startTime, endTime, response)
                        break
                    elif response[0] in map(str, range(10)) and not exchange:
                        try_booking = False
                        break
                    elif response == 'Failed':
                        time.sleep(2)
                        continue
                    else:
                        ddl = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=45, second=0)
                        delta = ddl - datetime.datetime.now()
                        print('\n连接丢失，1分钟后重新尝试抢座，系统开放时间剩余' + str(delta.seconds) + '秒\n')
                        time.sleep(60)
                        continue
                time.sleep(3)
            else:
                print('\n抢座失败，座位预约系统已关闭，开始尝试捡漏')
                SK.Wait(0, 59, 59, nextDay=True)
                response = SK.Loop(buildingId, rooms, startTime, endTime)
                if response[0] in map(str, range(10)) and exchange:
                    SK.ExchangeLoop(buildingId, startTime, endTime, response)
        print('\n抢座运行结束，等待下一轮循环')
    else:
        break
