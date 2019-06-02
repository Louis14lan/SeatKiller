# -*- coding: utf-8 -*-

import SeatKiller
import warnings
import getpass
import datetime
import time
import re
import sys
import random


class SeatKillerRunner:

    def __init__(self):
        self.buildingId = 1
        self.rooms = {}
        self.startTime = 480
        self.endTime = 1350
        self.roomId = "9"
        self.seatId = "61"

    def login(self):
        while True:
            username = "2018202110143"  # input('请输入学号：')
            password = "082931"  # getpass.getpass('请输入图书馆密码：')

            SK = SeatKiller.SeatKiller(username, password)

            if SK.GetToken():
                SK.GetUsrInf()
                print('登陆成功')
                return SK
                break
        return None

    def checkSeatInfo(self, SK):
        while True:
            res = SK.CheckResInf()
            if res == 'using':
                if input('\n是否释放此座位（1.是 2.否）：') == '1':
                    if not SK.StopUsing():
                        print('\n释放座位失败，请稍等后重试')
                        enableLoop = False
                        break
                else:
                    enableLoop = False
                    break
            elif res:
                if input('\n是否取消预约此座位（1.是 2.否）：') == '1':
                    if not SK.CancelReservation(res):
                        print('\n预约取消失败，请稍等后重试')
                        enableLoop = False
                        break
                else:
                    enableLoop = False
                    break
            else:
                break
        return res

    def checkLibary(self, SK):
        while True:
            buildingId = input('\n请输入分馆编号（1.信息科学分馆 2.工学分馆 3.医学分馆 4.总馆）：')
            if buildingId == '1':
                rooms = SK.xt
                if input('若抢到的座位位于\'一楼3C创客空间\'，是否尝试换座（1.是 2.否）：') == '1':
                    exchange = True
            elif buildingId == '2':
                rooms = SK.gt
            elif buildingId == '3':
                rooms = SK.yt
            elif buildingId == '4':
                rooms = SK.zt
            else:
                print('分馆编号输入不合法')
                continue
            self.buildingId = buildingId
            self.rooms = rooms
            break

    def inputTime(self):
        while True:
            startTimeStr = input('请输入开始时间（以分钟为单位，从0点开始计算，以半小时为间隔，08:00）：')

            startTime = (int)(startTimeStr[0:2]) * 2 * 30 + (int)(startTimeStr[3:5])
            self.startTime = str(startTime)
            if self.startTime in map(str, range(480, 1321, 30)):
                break
            else:
                print('开始时间输入不合法')

        while True:
            endTimeStr = input('请输入结束时间（以分钟为单位，从0点开始计算，以半小时为间隔，08:30）：')
            endTime = (int)(endTimeStr[0:2]) * 2 * 30 + (int)(endTimeStr[3:5])
            self.endTime = str(endTime)
            if self.endTime in map(str, range(int(self.startTime), 1351, 30)):
                break
            else:
                print('结束时间输入不合法')

    def choosePattern(self, enableLoop, exchange, res, SK):
        buildingId = self.buildingId
        rooms = self.rooms
        startTime = self.startTime
        endTime = self.endTime
        if enableLoop:
            if input('是否进入捡漏模式（1.是 2.否）：') == '1':
                response = SK.Loop(buildingId, rooms, startTime, endTime)
                if response[0] in map(str, range(10)) and exchange:
                    SK.ExchangeLoop('1', SK.xt_lite, startTime, endTime, response)
                sys.exit()
        else:
            if input('是否进入改签模式（1.是 2.否）：') == '1':
                SK.ExchangeLoop(buildingId, rooms, startTime, endTime, res)
                sys.exit()

    def getRoomId(self):
        buildingId = self.buildingId
        if buildingId == '1':
            roomId = input('已获取区域列表：\n'
                           '4.一楼3C创客空间\n'
                           '5.一楼创新学习讨论区\n'
                           '6.二楼西自然科学图书借阅区\n'
                           '7.二楼东自然科学图书借阅区\n'
                           '8.三楼西社会科学图书借阅区\n'
                           '9.四楼西图书阅览区\n'
                           '10.三楼东社会科学图书借阅区\n'
                           '11.四楼东图书阅览区\n'
                           '12.三楼自主学习区\n'
                           '14.3C创客-双屏电脑（20台）\n'
                           '15.创新学习-MAC电脑（12台）\n'
                           '16.创新学习-云桌面（42台）\n'
                           '请输入房间编号（若由系统自动选择请输入\'0\'）：')
        elif buildingId == '2':
            roomId = input('已获取区域列表：\n'
                           '19.201室-东部自科图书借阅区\n'
                           '29.2楼-中部走廊\n'
                           '31.205室-中部电子阅览室笔记本区\n'
                           '32.301室-东部自科图书借阅区\n'
                           '33.305室-中部自科图书借阅区\n'
                           '34.401室-东部自科图书借阅区\n'
                           '35.405室中部期刊阅览区\n'
                           '37.501室-东部外文图书借阅区\n'
                           '38.505室-中部自科图书借阅区\n'
                           '请输入区域编号（若由系统自动选择请输入\'0\'）：')
        elif buildingId == '3':
            roomId = input('已获取区域列表：\n'
                           '20.204教学参考书借阅区\n'
                           '21.302中文科技图书借阅B区\n'
                           '23.305科技期刊阅览区\n'
                           '24.402中文文科图书借阅区\n'
                           '26.502外文图书借阅区\n'
                           '27.506医学人文阅览区\n'
                           '请输入房间编号（若由系统自动选择请输入\'0\'）：')
        else:
            roomId = input('已获取区域列表：\n'
                           '39.A1-座位区\n'
                           '40.C1自习区\n'
                           '51.A2\n'
                           '52.A3\n'
                           '56.B3\n'
                           '59.B2\n'
                           '60.A4\n'
                           '61.A5\n'
                           '62.A1-沙发区\n'
                           '65.B1\n'
                           '66.A1-苹果区\n'
                           '请输入房间编号（若由系统自动选择请输入\'0\'）：')
        self.roomId = roomId

    def getSeatId(self, SK):
        roomId = self.roomId
        if roomId == '0':
            seatId = '0'
        else:
            date = datetime.date.today()
            date = date.strftime('%Y-%m-%d')
            if SK.GetSeats(roomId, date):
                seatName = input(
                    '请输入座位ID（范围：' + min(SK.allSeats.keys()) + '～' + max(SK.allSeats.keys()) + ' 若由系统自动选择请输入\'0\'）：')
                seatId = SK.allSeats.get(seatName)
            else:
                print('座位ID输入有误，将由系统自动选择')
                seatId = '0'
        self.seatId = seatId

    def killSeat(self, exchange, SK):
        buildingId = self.buildingId
        rooms = self.rooms
        startTime = self.startTime
        endTime = self.endTime
        roomId = self.roomId
        seatId = self.seatId
        while True:
            try_booking = True
            if datetime.datetime.now() < datetime.datetime.replace(datetime.datetime.now(), hour=22, minute=44,
                                                                   second=40):
                print('\n------------------------准备获取token------------------------')
                SK.Wait(22, 44, 40)
            else:
                print('\n------------------------开始获取token------------------------')
            date = datetime.date.today() + datetime.timedelta(days=1)
            date = date.strftime('%Y-%m-%d')
            print('\ndate:' + date)

            if SK.GetToken():
                SK.GetBuildings()
                SK.GetRooms(buildingId)
                if roomId != '0':
                    SK.GetSeats(roomId, date)

                if datetime.datetime.now() < datetime.datetime.replace(datetime.datetime.now(), hour=22, minute=45,
                                                                       second=0):
                    SK.Wait(22, 45, 0)
                elif datetime.datetime.now() > datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=45,
                                                                         second=0):
                    print('\n预约系统开放时间已过，准备进入捡漏模式')
                    SK.Wait(0, 59, 59, nextDay=True)
                    response = SK.Loop(buildingId, rooms, startTime, endTime)
                    if response[0] in map(str, range(10)) and exchange:
                        SK.ExchangeLoop('1', SK.xt_lite, startTime,
                                        endTime, response)
                    sys.exit()
                print('\n------------------------开始预约次日座位------------------------')
                while try_booking:
                    if seatId != '0':
                        if SK.BookSeat(seatId, date, startTime, endTime) not in ('Failed', 'Connection lost'):
                            break
                        else:
                            print('\n指定座位预约失败，尝试检索其他空位...')
                            seatId = '0'
                    elif datetime.datetime.now() < datetime.datetime.replace(datetime.datetime.now(), hour=23,
                                                                             minute=45,
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

                        if not SK.freeSeats:
                            print('\n当前全馆暂无空位，3-5秒后尝试继续检索空位')
                            time.sleep(random.uniform(3, 5))
                            continue

                        for freeSeatId in SK.freeSeats:
                            response = SK.BookSeat(
                                freeSeatId, date, startTime, endTime)
                            if response == 'Success':
                                try_booking = False
                                break
                            elif response[0] in map(str, range(10)) and exchange:
                                SK.ExchangeLoop('1', SK.xt_lite, startTime,
                                                endTime, response, nextDay=True)
                                try_booking = False
                                break
                            elif response[0] in map(str, range(10)) and not exchange:
                                try_booking = False
                                break
                            elif response == 'Failed':
                                time.sleep(random.uniform(1, 3))
                            else:
                                ddl = datetime.datetime.replace(
                                    datetime.datetime.now(), hour=23, minute=45, second=0)
                                delta = ddl - datetime.datetime.now()
                                print('\n连接丢失，1分钟后重新尝试抢座，系统开放时间剩余' +
                                      str(delta.seconds) + '秒\n')
                                time.sleep(60)
                    else:
                        print('\n抢座失败，座位预约系统已关闭，开始尝试捡漏')
                        SK.Wait(0, 59, 59, nextDay=True)
                        response = SK.Loop(buildingId, rooms, startTime, endTime)
                        if response[0] in map(str, range(10)) and exchange:
                            SK.ExchangeLoop('1', SK.xt_lite, startTime,
                                            endTime, response)
                print('\n抢座运行结束，2小时后进入下一轮循环')
                time.sleep(7200)
            else:
                print('\n登录失败，等待5秒后重试')
                time.sleep(5)

    def run(self):
        warnings.filterwarnings('ignore')
        enableLoop = True
        exchange = False

        # 登陆
        SK = self.login()

        # 检查预约状态是否已预约
        res = self.checkSeatInfo(SK)

        # 输入抢座分馆
        self.checkLibary(SK)

        # 输入预约时间
        self.inputTime()

        # 选择捡漏模式还是改签模式
        self.choosePattern(enableLoop, exchange, res, SK)

        # 获取roomId
        self.getRoomId()

        # 获取seatId
        self.getSeatId(SK)

        # 抢座
        print("开始抢票")
        self.killSeat(exchange, SK)


if __name__ == '__main__':
    seat = SeatKillerRunner()
    seat.run()
