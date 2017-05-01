# encoding=utf-8
# ----------------------------------------
# 语言：Python2.7
# 日期：2017-05-01
# 作者：九茶<http://blog.csdn.net/bone_ace>
# 功能：破解四宫格图形验证码，登录m.weibo.cn
# ----------------------------------------

import time
import random
from PIL import Image
import StringIO
from math import sqrt
from ims import ims
from selenium import webdriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.action_chains import ActionChains

PIXELS = [(465, 371), (566, 371), (465, 472), (566, 472)]


def getType(browser):
    """ 识别图形路径 """
    ttype = ''
    time.sleep(3.5)
    im = Image.open(StringIO.StringIO(browser.get_screenshot_as_png())).crop((400, 310, 630, 530)).convert('L')
    width = im.size[0]
    height = im.size[1]
    for png in ims.keys():
        isGoingOn = True
        for i in range(width):
            for j in range(height):
                if abs(im.load()[i, j] - ims[png][i][j]) > 10:
                    isGoingOn = False
                    break
            if isGoingOn is False:
                ttype = ''
                break
            else:
                ttype = png
        else:
            break
    return ttype


def move(browser, coordinate, coordinate0):
    """ 从坐标coordinate0，移动到坐标coordinate """
    time.sleep(0.05)
    length = sqrt((coordinate[0] - coordinate0[0]) ** 2 + (coordinate[1] - coordinate0[1]) ** 2)    # 两点直线距离
    if length < 4:  # 如果两点之间距离小于4px，直接划过去
        ActionChains(browser).move_by_offset(coordinate[0]-coordinate0[0], coordinate[1]-coordinate0[1]).perform()
        return
    else:   # 递归，不断向着终点滑动
        step = random.randint(3, 5)
        x = int(step * (coordinate[0] - coordinate0[0]) / length)   # 按比例
        y = int(step * (coordinate[1] - coordinate0[1]) / length)
        ActionChains(browser).move_by_offset(x, y).perform()
        move(browser, coordinate, (coordinate0[0]+x, coordinate0[1]+y))


def draw(browser, ttype):
    """ 滑动 """
    if len(ttype) == 4:
        px0 = PIXELS[int(ttype[0]) - 1]
        ActionChains(browser).move_by_offset(px0[0] - 516, px0[1] - 304).perform()
        browser.execute(Command.MOUSE_DOWN, {})

        px1 = PIXELS[int(ttype[1]) - 1]
        move(browser, (px1[0], px1[1]), px0)

        px2 = PIXELS[int(ttype[2]) - 1]
        move(browser, (px2[0], px2[1]), px1)

        px3 = PIXELS[int(ttype[3]) - 1]
        move(browser, (px3[0], px3[1]), px2)
        browser.execute(Command.MOUSE_UP, {})
    else:
        print 'Sorry! Failed! Maybe you need to update the code.'


if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.set_window_size(1050, 840)
    browser.get('https://passport.weibo.cn/signin/login?entry=mweibo&r=http://weibo.cn/')

    time.sleep(1)
    name = browser.find_element_by_id('loginName')
    psw = browser.find_element_by_id('loginPassword')
    login = browser.find_element_by_id('loginAction')
    name.send_keys('15200692422')   # 测试账号
    psw.send_keys('zckhm7071')
    login.click()

    ttpye = getType(browser)    # 识别图形路径
    print 'Result: %s!' % ttpye
    draw(browser, ttpye)    # 滑动破解
    time.sleep(20)
    browser.close()

