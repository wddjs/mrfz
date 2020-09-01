# -*- coding: utf-8 -*-

# @CreateTime : 2019/9/26
# @Author : Twitter@bakashigure
# @Site : https://github.com/bakashigure/mrfz
# @Software: 明日方舟代肝脚本


import ctypes
import msvcrt
import re
import time
import os
import base64
import sys
from io import BytesIO
from io import TextIOWrapper
from enum import Enum
from PIL import Image
import pyautogui as pag
import win32con, win32gui, win32ui, win32api

from imgbb import imgbase64c



class LOG:
    def __init__(self):
        self.log=[]
    def logging(self,str):
        if len(self.log)>=13:
            self.log.pop(0)
            self.log.append(str)
        else:
            self.log.append(str)
    def loggOutput(self):
        for items in self.log:
            print(items)
    def update(self,str):
        sb="["+str(currentTime())+"] ["+str+"]"
        return self.logging(sb)

ll=LOG()

def debug(info):
    def wrapper(func):
        def inner_wrapper(*args,**kwargs):
            
            sb='[{time}] [{info}] enter function {func}()'.format(
                time=currentTime(),
                info=info,
                func=func.__name__)
            ll.logging(sb)
            return func(*args,**kwargs)
        return inner_wrapper
    return wrapper


class IDIMG:
    def __init__(self):
        self.game_times = 0
        self.game_pid = 0
        self.game_kind = 1
        self.game_ann_kind = 1
        self.game_title = ""

        self.img_byte_success = base64.b64decode(imgbase64c.mission_success)
        self.img_success = BytesIO(self.img_byte_success)
        # self.img_success = Image.open(BytesIO(self.img_byte_success))

        self.img_byte_fail = base64.b64decode(imgbase64c.mission_fail)
        self.img_fail = BytesIO(self.img_byte_fail)
        # self.img_fail = Image.open(BytesIO(self.img_byte_fail))

        self.img_byte_ready = base64.b64decode(imgbase64c.mission_ready)
        self.img_ready = BytesIO(self.img_byte_ready)
        # self.img_ready = Image.open(BytesIO(self.img_byte_ready))

        self.img_byte_start = base64.b64decode(imgbase64c.mission_start)
        self.img_start = BytesIO(self.img_byte_start)
        # self.img_start = Image.open(BytesIO(self.img_byte_start))

        self.img_byte_auto_on = base64.b64decode(imgbase64c.mission_auto_on)
        self.img_auto_on = BytesIO(self.img_byte_auto_on)
        # self.img_on = Image.open(BytesIO(self.img_byte_auto_on))

        self.img_byte_auto_off = base64.b64decode(imgbase64c.mission_auto_off)
        self.img_auto_off = BytesIO(self.img_byte_auto_off)
        # self.img_off = Image.open(BytesIO(self.img_byte_auto_off))

        self.img_byte_playing = base64.b64decode(imgbase64c.mission_playing)
        self.img_playing = BytesIO(self.img_byte_playing)
        # self.img_playing = Image.open(BytesIO(self.img_byte_playing))

        self.img_byte_ann_chernob = base64.b64decode(imgbase64c.ann_chernob)
        self.img_ann_chernob = BytesIO(self.img_byte_ann_chernob)
        # self.img_ann_chernob=Image.open(BytesIO(self.img_byte_ann_chernob))

        self.img_byte_ann_downtown = base64.b64decode(imgbase64c.ann_downtown)
        self.img_ann_downtown = BytesIO(self.img_byte_ann_downtown)
        # self.img_ann_downtown=Image.open(BytesIO(self.img_byte_ann_downtown))

        self.img_byte_ann_outskirts = base64.b64decode(imgbase64c.ann_outskirts)
        self.img_ann_outskirts = BytesIO(self.img_byte_ann_outskirts)
        # self.img_ann_outskirts=Image.open(BytesIO(self.img_byte_ann_outskirts))

        self.img_byte_ann_success = base64.b64decode(imgbase64c.ann_success)
        self.img_ann_success = BytesIO(self.img_byte_ann_success)
        # self.imng_ann_success=Image.open(BytesIO(self.img_byte_ann_success))

        """
        self.list_all = [
            self.img_ready,
            self.img_start,
            self.img_playing,
            self.img_success,
            self.img_fail,
        ]
        """

        self.list_mainline = {
            self.img_byte_ready: "ready",
            self.img_byte_start: "start",
            self.img_byte_playing: "playing",
            self.img_byte_success: "success",
            self.img_byte_fail: "fail",
        }

        self.list_mainlinetest={
            self.img_ready:"ready",
            self.img_start:"ready",
            self.img_playing:"playing",
            self.img_success:"success",
            self.img_fail:"fail",
        }


        self.list_ann_level = [
            self.img_byte_ann_chernob,
            self.img_byte_ann_downtown,
            self.img_byte_ann_outskirts,
        ]

        self.list_ann = {
            self.img_ready: "ready",
            self.img_start: "start",
            self.img_playing: "playing",
            self.img_ann_success: "success",
        }

    @debug(info="获取游戏截图")
    def getAppScreenshot(self):
        try:
            pid = int(self.game_pid)
            left, top, right, bot = win32gui.GetWindowRect(pid)
            width = right - left
            height = bot - top
            '''
            print(
                "__log__: ",
                "left: ",
                left,
                "  top: ",
                top,
                "  right: ",
                right,
                "  bottom: ",
                bot,
            )
            print("__log__: ", "width: ", width, "  height: ", height)
            '''
            hWndDC = win32gui.GetWindowDC(pid)
            mfcDC = win32ui.CreateDCFromHandle(hWndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            saveDC.SelectObject(saveBitMap)
            saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            im_PIL = Image.frombuffer(
                "RGB",
                (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
                bmpstr,
                "raw",
                "BGRX",
                0,
                1,
            )
            return im_PIL, left, width, top
        except:
            print("出现神必错误。")
            msvcrt.getch()
            os._exit(1)

    def locateMainline(self, screenshots, width, height):
        for items, ide in self.list_mainline.items():
            img = Image.open(BytesIO(items))
            img = img.resize(
                (int(width / 1440 * img.size[0]), int(width / 1440 * img.size[1])),
                Image.ANTIALIAS,
            )
            if (res := pag.locate(img, screenshots, confidence=0.8)) != None:
                print(img.size[0], img.size[1])
                print(res)
                return ide


    @debug(info="定位主线")
    def locateMainlineTest(self):
        screenshot, _left, width, _top=self.getAppScreenshot()
        for items,value in self.list_mainlinetest.items():
            img=Image.open(items)
            img=img.resize((int(width / 1440 * img.size[0]), int(width / 1440 * img.size[1])),
                Image.ANTIALIAS,)
            if(res:=pag.locate(img,screenshot,confidence=0.8))!=None:
                position=[]
                position.append(pag.center(res)[0])
                position.append(pag.center(res)[1])
                print(img.size[0], img.size[1])
                print(res)
                print("position",position[0],"  ",position[1])
                return value,position
        return None,None


    @debug(info="定位剿灭")
    def locateAnn(self):
        screenshot, left, width, top=self.getAppScreenshot()
        for items,value in self.list_ann.items():
            img=Image.open(items)
            img=img.resize((int(width / 1440 * img.size[0]), int(width / 1440 * img.size[1])),
                Image.ANTIALIAS,)
            if(res:=pag.locate(img,screenshot,confidence=0.8))!=None:
                position=[]
                position.append(pag.center(res)[0]-left)
                position.append(pag.center(res)[1]-top)
                #print(img.size[0], img.size[1])
                #print(res)
                return value,position
        return None,None

    def locateAuto(self):
        _screenshot, _left, _width, _top=self.getAppScreenshot()
        img = Image.open(self.img_auto_off)
        img = img.resize(
            (int(_width / 1440 * img.size[0]), int(_width / 1440 * img.size[1])),
            Image.ANTIALIAS,
        )
        if pag.locate(img, _screenshot, confidence=0.8) != None:
            return False
        return True


class GAMEKINDS(Enum):
    主线或材料 = 1
    剿灭 = 2
    活动 = 3
    切尔诺伯格 = 4
    龙门外环 = 5
    龙门市区 = 6


class UI:
    @debug(info="初始化ui")
    def __init__(self, title, hwnd, kind, times):
        self.hwnd = hwnd
        self.title = title
        self.kind = kind
        self.times = times
    @debug(info="更新ui")
    def update(self, current_cnt, msg):
        os.system("cls")
        print( f"""
    ⣿⣿⡟⠁⠄⠟⣁⠄⢡⣿⣿⣿⣿⣿⣿⣦⣼⢟⢀⡼⠃⡹⠃⡀⢸⡿⢸⣿⣿⣿⣿⣿⡟
    ⣿⣿⠃⠄⢀⣾⠋⠓⢰⣿⣿⣿⣿⣿⣿⠿⣿⣿⣾⣅⢔⣕⡇⡇⡼⢁⣿⣿⣿⣿⣿⣿⢣
    ⣿⡟⠄⠄⣾⣇⠷⣢⣿⣿⣿⣿⣿⣿⣿⣭⣀⡈⠙⢿⣿⣿⡇⡧⢁⣾⣿⣿⣿⣿⣿⢏⣾      明日方舟代肝脚本 Version2.1 build0901.2355
    ⣿⡇⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⠇⠄⠄⢿⣿⡇⢡⣾⣿⣿⣿⣿⣿⣏⣼⣿      https://github.com/bakashigure/mrfz
    ⣿⣷⢰⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣧⣀⡄⢀⠘⡿⣰⣿⣿⣿⣿⣿⣿⠟⣼⣿⣿
    ⢹⣿⢸⣿⣿⠟⠻⢿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣉⣤⣿⢈⣼⣿⣿⣿⣿⣿⣿⠏⣾⣹⣿⣿
    ⢸⠇⡜⣿⡟⠄⠄⠄⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟⣱⣻⣿⣿⣿⣿⣿⠟⠁⢳⠃⣿⣿⣿
    ⠄⣰⡗⠹⣿⣄⠄⠄⠄⢀⣿⣿⣿⣿⣿⣿⠟⣅⣥⣿⣿⣿⣿⠿⠋⠄⠄⣾⡌⢠⣿⡿"


    正在监视进程: {self.hwnd}  {self.title} |  当前时间 {currentTime()}
    关卡种类: {self.kind} , 正在进行第{current_cnt+1}次，共{self.times}次
    状态:{msg}

    """
        )
        for items in ll.log:
            print(items)

        # sys.stdout.flush()


# 摸鱼time
@debug("摸鱼")
def sleep(sec):
    time.sleep(sec)


# 获取当前窗口句柄
@debug("获取当前窗口句柄")
def currentHwnd():
    return win32gui.GetForegroundWindow()


# 切换进程并置顶
@debug("切换进程并置顶")
def switchHwnd(hwnd):
    try:
        ctypes.windll.user32.SwitchToThisWindow(hwnd, True)
    except:
        pass
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNA)
    except:
        pass
    try:
        win32api.keybd_event(13, 0, 0, 0)  # 发送一次回车事件，不然无法置顶游戏窗口 这也算是神秘bug之一吧
        win32gui.SetForegroundWindow(hwnd)
    except:
        pass


# 当前时间

def currentTime():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))


# 先行枚举句柄
@debug("初始化")
def init():

    hwnd_title = dict()

    def getAllHwnd(hwnd, mouse):
        if (
            win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd)
        ):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(getAllHwnd, 0)

    game_lists = []
    for h, t in hwnd_title.items():
        if t != "":
            c = f"{h} {t}"
            result = re.match(r"([0-9]*) (.*)模拟器(.*)", c, flags=0)
            if result != None:
                game_lists.append(result)

    if (n := len(game_lists)) == 0:

        for h, t in hwnd_title.items():
            if t != "":
                print(" |", "%-10s" % h, "%.50s" % t)
        print("\n未找到包含'模拟器'字样的游戏进程,请手动指定进程hwnd")
        print("例子: 如您看到[   | 114514 MuMu模拟器   ]，请输入114514")
        hwnd = eval(input("请打开模拟器后重试,或手动输入hwnd(进程名前的数字):"))
        name = hwnd_title[hwnd]
        return hwnd, name

    elif n == 1:
        print("找到了一个可能是模拟器的进程[ ", game_lists[0].group(0), " ]")
        case = eval(input("是它吗? 输入1确定，输入0手动指定进程:"))
        if case == 1:
            name = hwnd_title[int(game_lists[0].group(1))]
            return game_lists[0].group(1), name
        elif case == 0:
            for h, t in hwnd_title.items():
                if t != "":
                    print(" |", "%-10s" % h, "%.50s" % t)
            hwnd = eval(input("手动输入hwnd(进程名前的数字):"))
            name = hwnd_title[hwnd]
            return hwnd, name

    elif n > 1:
        print("找到了多个包含模拟字样的进程，您可能想多开? 请手动指定进程hwnd(进程名前的数字)")
        for h, t in hwnd_title.items():
            if t != "":
                print(" |", "%-10s" % h, "%.50s" % t)
        hwnd = eval(input("手动输入hwnd(进程名前的数字):"))
        name = hwnd_title[hwnd]
        return hwnd, name


def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False



def main():
    os.system("title 明日方舟代刷脚本V2.0 twitter@bakashigure")
    print(
        """ ####预览版本 未正式发布####
    
    欢迎使用明日方舟刷图脚本 Version2.0
    这里是一些程序说明，请仔细阅读后使用。

    0.本程序会先试图遍历进程寻找包含模拟器三字的进程，如果结果为0，则会让您自行指定进程，
       如果结果为1，则会向您确认是否为游戏进程，如果结果大于1，则会让您手动指定进程.
       随后需要您指定主线/剿灭,将游戏打开到右下角为开始行动的蓝色字样，
       勾选代理作战,随后在本程序内输入您希望循环刷图的次数.
       随后在软件内确认开始后，会自动进行识别刷图.
       游戏可以放在后台，但请不要最小化.

    1.本程序需要管理员权限，这是因为模拟鼠标点击所需，您也可以通过Github上的开源代码自己在IDE中运行.
    2.本程序支持多开，请自行指定正确的进程句柄.
    3.本软件工作原理是通过对处于后台/前台的游戏窗口进行截图并识别当前状态，不会对游戏进程进行任何的操作.
    4.建议分辨率1440*810，可以缩放窗口，但过大或过小的窗口可能造成识别失败.
    6.几乎没有错误处理，所以请不要在输入数字的地方输入其他字符.
    7.目前仅支持[简体中文]的游戏内容



    附0: 开源项目地址 https://github.com/bakashigure/mrfz  (请不要用于商业化)
    附1: 我的官服id 孭纸#416  (孭读mie)
    附2: contact::bakashigure@hotmail.com

    如您已阅读完毕，请按任意键继续.
    """
    )

    msvcrt.getch()
    os.system("cls")
    if isAdmin():
        pass
    else:
        print("鼠标点击需要管理员权限，请以管理员权限运行重试.")
        print("按任意键退出.")
        msvcrt.getch()
        os._exit(1)

    sb = IDIMG()
    sb.game_pid, sb.game_title = init()
    #print(sb.game_pid)
    sb.game_kind = eval(input("请输入关卡种类:  1.[主线/材料]   2.[剿灭] "))
    if sb.game_kind == 2:
        sb.game_ann_kind = eval(input("请输入剿灭关卡:  1.[切尔诺伯格]   2.[龙门外环]   3.[龙门市区]"))
    sb.game_times = eval(input("请输入代刷的次数(当前体力/每关耗体): "))
    if sb.game_kind == 1:
        ui = UI(sb.game_pid, sb.game_title, GAMEKINDS(sb.game_kind).name, sb.game_times)
    else:
        _gamekinds = (
            str(GAMEKINDS(sb.game_kind).name)
            + "-"
            + str(GAMEKINDS(sb.game_ann_kind + 3).name)
        )
        ui = UI(sb.game_pid, sb.game_title, _gamekinds, sb.game_times)

    for t in range(sb.game_times):
        while 1:
            if sb.game_kind == 1:
                result,position = sb.locateMainlineTest()
                if result==None:
                    ui.update(t, "未识别到内容，正在尝试下一次识别")
                    sleep(2)

                elif result == "ready":

                    os.system("cls")
                    if (
                        sb.locateAuto()== False
                    ):
                        ui.update(t, "您未开启代理诶，自己勾一下吧")
                        ll.update("定位代理")
                        sleep(2)
                        continue
                    ui.update(t, "已找到蓝色开始行动按钮，即将进行下一步")
                    ll.update("定位蓝色开始行动")
                    sleep(2)
                    pclick(sb.game_pid,position)
                    """
                    else:
                        os.system("cls")
                        ui.update(1, '请打开到右下角蓝色"开始行动"按钮，会自动识别。')
                    sleep(2)
                    """

                elif result == "start":
                    ui.update(t, "已找到红色开始行动按钮，即将进行下一步")
                    ll.update("定位红色开始行动")
                    sleep(2)
                    pclick(sb.game_pid,position)
                    print(result)

                elif result == "playing":
                    ui.update(t, "代理指挥作战正常运行中...")
                    ll.update("代理指挥正常运行")
                    sleep(2)

                elif result == "success":
                    ui.update(t, "本关已完成，即将进行下一次.")
                    ll.update("本关已完成")
                    pclick(sb.game_pid,position)
                    sleep(2)
                    break


            elif sb.game_kind == 2:
                """
                _ann_flag=1
                im_PIL, left, width, top, height = getAppScreenshot(sb.game_pid)
                ann=sb.locateAuto(sb.list_ann_level[sb.game_ann_kind-1],im_PIL,width,height)
                if ann == False and _ann_flag==0:
                    ui.update(t,f"已找到{GAMEKINDS(sb.game_ann_kind+3).name},即将进行下一步操作")
                    _ann_flag=1
                    sleep(2)
                    msvcrt.getch()
                elif ann == True and _ann_flag==0:
                    ui.update(t,f"未找到{GAMEKINDS(sb.game_ann_kind+3).name},请重试")
                    sleep(2)
                    continue
                """


                result,position = sb.locateAnn()
                if result == "ready":
                    os.system("cls")
                    if (
                        sb.locateAuto()== False
                    ):
                        ui.update(t, "您未开启代理诶，自己勾一下吧")
                        sleep(2)
                        continue
                    ui.update(t, "已找到蓝色开始行动按钮，即将进行下一步")
                    sleep(1)
                    pclick(sb.game_pid,position)

                elif result == "start":
                    pclick(sb.game_pid,position)
                    print(result)

                elif result == "playing":
                    ui.update(t, "代理指挥作战正常运行中...")
                    sleep(2)

                elif result == "success":
                    ui.update(t, "本关已完成，即将进行下一次.")
                    pclick(sb.game_pid,position)
                    sleep(1)
                    break

                else:
                    ui.update(t, "未识别到内容，正在尝试下一次识别")
                    sleep(2)

    ui.update(t, "本次代理指挥作战已全部完成，感谢使用!")
@debug("尝试点击")
def pclick(hwnd,position):
    hwnd=int(hwnd)
    p=win32api.MAKELONG(position[0],position[1])
    win32gui.SendMessage(hwnd,win32con.WM_ACTIVATE,win32con.WA_ACTIVE,0)
    win32api.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,p)
    sleep(0.05)
    win32api.SendMessage(hwnd,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,p)
    sleep(0.05)
if __name__ == "__main__":
    main()
