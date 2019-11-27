#!/usr/bin/env python3
from gevent import monkey

monkey.patch_all()
import gevent
import urllib.request
import requests
import os
import time
import datetime
import random
import re
from queue import Queue
import cv2
import numpy as np
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from aip import AipOcr

# from PyQt5.QtCore import QThread

requests.packages.urllib3.disable_warnings()
BASE_URL = 'https://appointment.bmeia.gv.at/'
SERV_URL = 'http://localhost:5555/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
}
TOKEN_PATTERN = re.compile(r'<input id="Token" name="Token" type="hidden" value="(.*?)"')
BAIDU_OCR_OPTIONS = {}
BAIDU_OCR_OPTIONS["recognize_granularity"] = "small"
BAIDU_OCR_OPTIONS["detect_direction"] = "true"
G_Q_OCR = Queue()
G_CLIENTS = []
G_PEKING_CLIENTS = []
G_SHANGHAI_CLIENTS = []
G_PEKING_CLIENTS_DEBUG = []
G_SHANGHAI_CLIENTS_DEBUG = []
G_DEBUG = False


def fetchClients():
    """
    从服务器获取客户信息,并分类(北京、上海、北京调试、上海调试)
    """
    global G_DEBUG, G_PEKING_CLIENTS, G_SHANGHAI_CLIENTS, G_PEKING_CLIENTS_DEBUG, G_SHANGHAI_CLIENTS_DEBUG
    # """
    r = requests.get(f'{SERV_URL}clients', headers=HEADERS)
    if r.status_code == 200:
        res = r.json()
        if res['status'] == 'ok':
            clients = res['data']
            flag = False
            for client in clients['PEKING']:
                CalendarId = client['CalendarId']
                if CalendarId == '1213873' or CalendarId == '950653':
                    flag = True
                    G_PEKING_CLIENTS_DEBUG.append(client)
                else:
                    G_PEKING_CLIENTS.append(client)
            for client in clients['SHANGHAI']:
                CalendarId = client['CalendarId']
                if CalendarId == '1213873' or CalendarId == '950653':
                    flag = True
                    G_SHANGHAI_CLIENTS_DEBUG.append(client)
                else:
                    G_SHANGHAI_CLIENTS.append(client)
            # TODO: 其他Office就在这里添加相应的!!
            # print('G_PEKING_CLIENTS: ', G_PEKING_CLIENTS)
            # print('G_SHANGHAI_CLIENTS: ', G_SHANGHAI_CLIENTS)
            # print('G_PEKING_CLIENTS_DEBUG: ', G_PEKING_CLIENTS_DEBUG)
            # print('G_SHANGHAI_CLIENTS_DEBUG: ', G_SHANGHAI_CLIENTS_DEBUG)
            if flag:
                # 只要clients中有一个演示的,都设置默认G_DEBUG为True,让使用者自己选择使用模式
                G_DEBUG = True if input('请输入运行模式([输入数字1]演示模式、[输入其他]正式模式): ') == '1' else False
            return True
        else:
            print('err')
    else:
        print('服务器访问失败')
    """
    G_SHANGHAI_CLIENTS.append({
        'CalendarType': 'SHANGHAI',
        'StartTime': '2/1/2020',
        'Firstname': 'JIAN',
        'Lastname': 'YAO',
        'DateOfBirth': '17.06.1975',
        'TraveldocumentNumber': 'E70681011',
        'Sex': '1',
        'Street': '1104building9,xidi international district',
        'Postcode': '210019',
        'City': 'Nanjing',
        'Country': '46',
        'Telephone': '18702194830',
        'Email': 'harry_humail@hotmail.com',
        'LastnameAtBirth': 'YAO',
        'NationalityAtBirth': '49',
        'CountryOfBirth': '49',
        'PlaceOfBirth': 'JIANGSU',
        'NationalityForApplication': '49',
        'TraveldocumentDateOfIssue': '23.06.2016',
        'TraveldocumentValidUntil': '22.06.2026',
        'TraveldocumentIssuingAuthority': '49',
    })
    return True
    """


def setBaiduOCRClients(filepath):
    """
    从文本文件读取百度OCR客户端
    :param filepath: 文本文件的路经
    """
    with open(filepath, 'r', encoding='utf-8') as fp:
        text = fp.read()
        lines = text.split('\n')
        for line in lines:
            if line:
                ps = line.split(' ')
                APP_ID = ps[0]
                API_KEY = ps[1]
                SECRET_KEY = ps[2]
                r = requests.post(f'{SERV_URL}baiduClients', data={
                    'APP_ID': APP_ID,
                    'API_KEY': API_KEY,
                    'SECRET_KEY': SECRET_KEY,
                })
                if r.status_code != 200:
                    print('上传百度OCR帐号失败!')
                    break


def fetchBaiduOCRClients(start=0, end=5):
    """
    r = requests.get(f'{SERV_URL}baiduClients/{start}/{end}', headers=HEADERS)
    if r.status_code == 200:
        clients = r.json()['data']
        global G_Q_OCR
        for client in clients:
            baidu_ocr_client = AipOcr(client['APP_ID'], client['API_KEY'], client['SECRET_KEY'])
            G_Q_OCR.put(baidu_ocr_client)
            # print(client)
        return True
    """
    # ------------------------------------------------------------
    global G_Q_OCR
    APP_ID = '16232754'
    API_KEY = '6peGW76zeFyRB9QmYUdDBRrW'
    SECRET_KEY = '1VXMjpITrniaXMp9tTkqHOmdVgiBcd1S'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16667240'
    API_KEY = 'kGdWqRmYqCvMMAtwRmyi3gcr'
    SECRET_KEY = 'kUx6tQ699OGf27SLvWkPxpWYbEUjpaxF'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16667411'
    API_KEY = 'MO31imWKDp5uD4blCoelC3SG'
    SECRET_KEY = 'XEftlFpcxDmD0NM4DPICiun0ydBTYHPy'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16667478'
    API_KEY = 'dyrn8EIcBa97q3gSjQS3SpT7'
    SECRET_KEY = '5Cs6fReXyF8jeEjcquWx4R3vyZlTwtK7'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16668509'
    API_KEY = 'hTIi04vTlR6ka0kdD7CLveL0'
    SECRET_KEY = 'TOfS1mVAt7SeizseffqAZpKBPnWuOAoV'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16850942'
    API_KEY = 'QmDoi0uNCNycHjGl7xpAjIY3'
    SECRET_KEY = 'E6Qm7YFbMNsVvIxNql0SU7VbKXLm1ovc'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16850943'
    API_KEY = 'rCe4ZXDuegUaCqCPIT1s9zTK'
    SECRET_KEY = 'R08Khxcrz4Ox66PGOQVNke7HY9snBiTz'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16850944'
    API_KEY = 'xuPzEQsjgbKn4mezV0DLVvcC'
    SECRET_KEY = 'SYO30yjpADFRdlM3596GKakrUlPifDQo'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16850945'
    API_KEY = 'rLFDYB8uoLnPr5UqPZBSCaVl'
    SECRET_KEY = 'bcUgs2V9HnPNWqB6rIZojHDvg4rK8TxQ'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16850946'
    API_KEY = 'vlGEIZXImmwYb3fjHC3VkC7Q'
    SECRET_KEY = 'LOZ8Si11rMDMrrPW2Oony7wpsFAcaRFA'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16850948'
    API_KEY = 'T9k37200VOVUZzbw2nHT2Qb6'
    SECRET_KEY = 'ld0Gk5dA4UvHlV5gU9GOZRM0y27ScgZx'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16850949'
    API_KEY = 'db2lq5quwtVwuVthK7t5dE2Y'
    SECRET_KEY = 'GGtqtbpvNj2zoMSaomiXLhj1O4LHNtQE'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16850950'
    API_KEY = 'oxHOlryYwx0wMUKEDij49ma3'
    SECRET_KEY = 'zrzFd0aOZGgOQDKEZIgs1O9esGSkFWhW'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16850951'
    API_KEY = '200r3TiG24dK8PDO60Mi5LCl'
    SECRET_KEY = 'nkI8pNQG8nGG6DiiBX5yrPk1zQKF61x8'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    # ------------------------------------------------------------
    APP_ID = '16850953'
    API_KEY = 'sMTbLUC5IFkNzG4s7nH7zHEI'
    SECRET_KEY = 'Qz4oU0xYy9hl5vVGgGpuCPDL1vCnh0Qa'
    baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    G_Q_OCR.put(baidu_ocr_client)
    return True


def loopFetchAndSetUnknownCalendarId(office):
    """
    正式上线时调用!用户不断地获取上海CalendarId,直至获取成功后才开始抢上海部分
    :return:
    """
    # TIPS: 上线时记得换成 Niederlassung
    keyword = 'Niederlassung'  # 到时候要抓取的关键字
    # keyword = '长达6个月'  # 到时候要抓取的关键字
    url = f'{BASE_URL}?office={office}'
    """
    playload = {
        'Language': 'zh',
        'Command': '变更',
        'Office': office,
        'CalendarId': '0',
    }
    """
    pattern = re.compile(r'<option value="(.*?)">.*?%s.*?</option>' % keyword.replace('"', '&quot;'))
    print('开始抓取上海的CalendarId')
    while True:
        try:
            # r = requests.post(url, data=playload, headers=HEADERS)
            r = requests.get(url, headers=HEADERS)
            if r.status_code == 200:
                text = r.text
                searchResult = re.search(pattern, text)
                if searchResult:
                    CalendarId = searchResult.group(1)
                    print(CalendarId)
                    global G_SHANGHAI_CLIENTS
                    for i in len(G_SHANGHAI_CLIENTS):
                        G_SHANGHAI_CLIENTS[i]['CalendarId'] = CalendarId
                    print('new G_SHANGHAI_CLIENTS: ', G_SHANGHAI_CLIENTS)
                    return True
        except Exception as e:
            print(e)
            pass


def getMondayInLastWeek(_t):
    """
    给一个"月/日/年 时:分"格式的日期字符串,返回这个日期的这个星期的星期一的日期
    :param t: '8/10/2019 10:20'
    :return: 星期一的日期   '日/月/年 0:00:00'
    """
    dt = datetime.datetime.strptime(_t, '%d/%m/%Y %H:%M')
    diff = dt.weekday()
    for _ in range(diff + 7):
        dt = dt - datetime.timedelta(days=1)
    return f'{dt.day}/{dt.month}/{dt.year} 0:00:00'


def naive_remove_noise(cv2_image, k):
    """
    8邻域降噪
    Args:
        # image_name: 图片文件命名
        cv2_image: cv2
        k: 判断阈值
    Returns:
    """

    def calculate_noise_count(img_obj, w, h):
        """
        计算邻域非白色的个数
        Args:
            img_obj: img obj
            w: width
            h: height
        Returns:
            count (int)
        """
        count = 0
        width, height = img_obj.shape
        for _w_ in [w - 1, w, w + 1]:
            for _h_ in [h - 1, h, h + 1]:
                if _w_ > width - 1:
                    continue
                if _h_ > height - 1:
                    continue
                if _w_ == w and _h_ == h:
                    continue
                if img_obj[_w_, _h_] < 230:  # 二值化的图片设置为255
                    count += 1
        return count

    # img = cv2.imread(image_name, 1)
    # img = img_obj
    # 灰度
    # gray_img = cv2.cvtColor(img_obj, cv2.COLOR_BGR2GRAY)
    # gray_img = img_obj
    gray_img = cv2_image
    w, h = gray_img.shape
    for _w in range(w):
        for _h in range(h):
            if _w == 0 or _h == 0:
                gray_img[_w, _h] = 255
                continue
            # 计算邻域pixel值小于255的个数
            pixel = gray_img[_w, _h]
            if pixel == 255:
                continue
            if calculate_noise_count(gray_img, _w, _h) < k:
                gray_img[_w, _h] = 255
    return gray_img
    # return cv2.imencode('.png', gray_img)[1]


def baidu_ocr(img_bytes):
    baidu_ocr_client = G_Q_OCR.get()
    res = baidu_ocr_client.numbers(img_bytes, BAIDU_OCR_OPTIONS)
    # print(res)
    G_Q_OCR.put(baidu_ocr_client)
    # res = json.loads(res)
    words_result = res.get('words_result')
    if words_result:
        words = words_result[0].get('words')
        if words and len(words) == 4:
            return words
    return False


def fetchStartTimes(client, targetDay):
    """
    返回目标日期的所有可预约时间段
    :param client:
    :param targetDay: 日/月/年
    :return:
    """
    urlFirst = f'{BASE_URL}?fromSpecificInfo=True'  # 第一次进入先获取一次没有的话就用下面的获取下一周/上一周(改Monday可以跳)
    urlOther = f'{BASE_URL}HomeWeb/Scheduler'
    targetStartTimePattern = re.compile(r'input .*?%s.*?value="(.*?)"' % targetDay)
    playloadFirst = {
        'Language': 'zh',
        'Office': client['CalendarType'],
        'CalendarId': client['CalendarId'],
        'PersonCount': '1',
        'Command': '下一步',
    }
    playloadOther = {
        'Language': 'zh',
        'Office': client['CalendarType'],
        'CalendarId': client['CalendarId'],
        'PersonCount': '1',
        'Monday': getMondayInLastWeek(f'{targetDay} 10:30'),
        'Command': '下一周',
    }
    # print(getMondayInLastWeek(f'{targetDay} 10:30'))
    """
    r = requests.post(urlFirst, data=playloadFirst, headers=HEADERS)
    if r.status_code == 200:
        text = r.text
        if targetDay in text:
            searchResult = re.findall(targetStartTimePattern, text)
            if searchResult:
                # FIXME: 获取所有的StartTime
                # StartTime = searchResult.group(1)
                print(searchResult)
        else:
            r = requests.post(urlOther, data=playloadOther, headers=HEADERS)
            if r.status_code == 200:
                text = r.text
                searchResult = re.findall(targetStartTimePattern, text)
                if searchResult:
                    # FIXME: 获取所有的StartTime
                    # StartTime = searchResult.group(1)
                    print(searchResult)
        """
    while True:
        try:
            r = requests.post(urlOther, data=playloadOther, headers=HEADERS)
            if r.status_code == 200:
                text = r.text
                # with open('startTime.html', 'w', encoding='utf-8') as fp:
                #     fp.write(text)
                findResult = re.findall(targetStartTimePattern, text)
                if findResult:
                    return findResult
        except Exception as e:
            print(e)
            pass


def fetchToken(client, StartTime):
    url = f'{BASE_URL}HomeWeb/Scheduler'
    playload = {
        'Language': 'zh',
        'Office': client['CalendarType'],
        'CalendarId': client['CalendarId'],
        'PersonCount': '1',
        # 'Monday': '',  # 测试过,这个字段不需要的
        # 'Start': f'{StartTime}:00',
        'Start': StartTime,
        'Command': '下一步',
    }
    while True:
        try:
            r = requests.post(url, data=playload, headers=HEADERS)
            if r.status_code == 200:
                text = r.text
                with open('token.html', 'w', encoding='utf-8') as fp:
                    fp.write(text)
                searchResult = re.search(TOKEN_PATTERN, text)
                if searchResult:
                    Token = searchResult.group(1)
                    return Token
        except Exception as e:
            print(e)
            pass


def downloadCaptcha(Token):
    """
    重大发现!!!验证码的图片,只要token能用,每次请求的验证码内容都是一样的!ocr识别失败的话,再次请求一次就OK
    :param Token:
    :return: {'url': url, 'contentOri': content, 'contentNew': gray_content}
    """
    url = f'{BASE_URL}/Captcha?token={Token}'
    while True:
        try:
            r = requests.get(url, stream=True, headers=HEADERS)
            if r.status_code == 200:
                content = r.content
                # 新处理方式,试试?!
                gray_img = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_GRAYSCALE)
                blur = cv2.GaussianBlur(gray_img, (5, 5), 0)
                ret3, image = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                # ...
                gray_img = naive_remove_noise(image, 4)
                # gray_img = naive_remove_noise(content, 4)
                gray_content = cv2.imencode('.png', gray_img)[1]
                # with open('captcha1.png', 'wb') as fp:
                #     fp.write(content)
                # with open('captcha2.png', 'wb') as fp:
                #     fp.write(gray_content)
                return {'url': url, 'contentOri': content, 'contentNew': gray_content}
        except Exception as e:
            print(e)
            pass


def verificationCaptcha(captchaDict, captchaType):
    captchaImg = captchaDict['contentNew'] if captchaType == 0 else captchaDict['contentOri']
    try:
        CaptchaText = baidu_ocr(captchaImg)
        print('CaptchaText: ', CaptchaText)
        return CaptchaText
    except Exception as e:
        print(e)
        return False


def submit(client, StartTime, Token, CaptchaText):
    url = f'{BASE_URL}HomeWeb/Appointment'
    playload = {
        'Office': client['CalendarType'],
        'Language': 'zh',
        'CalendarId': client['CalendarId'],
        'Token': Token,
        'PersonCount': '1',
        # 'StartTime': f'{StartTime}:00',
        'StartTime': f'{StartTime}',
        'Lastname': client['Lastname'],
        'Firstname': client['Firstname'],
        'DateOfBirth': client['DateOfBirth'],
        'TraveldocumentNumber': client['TraveldocumentNumber'],
        'Sex': client['Sex'],
        'Street': client['Street'],
        'Postcode': client['Postcode'],
        'City': client['City'],
        'Country': client['Country'],
        'Telephone': client['Telephone'],
        'Email': client['Email'],
        'LastnameAtBirth': client['LastnameAtBirth'],
        'NationalityAtBirth': client['NationalityAtBirth'],
        'CountryOfBirth': client['CountryOfBirth'],
        'PlaceOfBirth': client['PlaceOfBirth'],
        'NationalityForApplication': client['NationalityForApplication'],
        'TraveldocumentDateOfIssue': client['TraveldocumentDateOfIssue'],
        'TraveldocumentValidUntil': client['TraveldocumentValidUntil'],
        'TraveldocumentIssuingAuthority': client['TraveldocumentIssuingAuthority'],
        'DSGVOAccepted': 'true',
        'CaptchaText': CaptchaText,
        'Command': '下一步',
    }
    while True:
        try:
            r = requests.post(url, data=playload, headers=HEADERS)
            if r.status_code == 200:
                text = r.text
                with open('result.html', 'w', encoding='utf-8') as fp:
                    fp.write(text)
                return text
        except Exception as e:
            print(e)
            pass


def coroutineTask(client, StartTime):
    print(f'    -[协程开始 {StartTime}]')
    while True:
        Token = fetchToken(client, StartTime)
        # print(Token)
        while True:  # 死循环,直至验证码识别结果为4个数字为止
            captchaDict = downloadCaptcha(Token)
            CaptchaText = verificationCaptcha(captchaDict, 0)
            if CaptchaText:
                break
        rText = submit(client, StartTime, Token, CaptchaText)
        if '预约成功' in rText:
            print(f'☺预约成功! [护照号码: {client["TraveldocumentNumber"]} 时间: {StartTime}]')
            return True
        elif '此时间已有其他预约' in rText:
            print(f'预约失败,此时间已有其他预约! [护照号码: {client["TraveldocumentNumber"]} 时间: {StartTime}]')
            return False
        elif '您已经有一个预约' in rText:
            print(f'恭喜!该客户已经成功预约了一个时间!不需要重复预约了! [护照号码: {client["TraveldocumentNumber"]}]')
            return False
        elif '您所输入的与图像中的文字不符' in rText:
            print('您所输入的与图像中的文字不符 重新抓取')


def threadTask(client):
    print(f'-[线程开始 {client["StartTime"]}]')
    targetDays = client['StartTime'].split(' ')
    startTimes = []
    for targetDay in targetDays:
        tmpStartTimes = fetchStartTimes(client, targetDay)
        startTimes += tmpStartTimes
    # greenlets = [gevent.spawn(coroutineTask, client, StartTime) for StartTime in client['StartTime'].split(', ')]
    greenlets = [gevent.spawn(coroutineTask, client, StartTime) for StartTime in startTimes]
    gevent.joinall(greenlets)
    print('线程结束')


# class Thread(QThread):
#     def __init__(self, client):
#         self.client = client
#         super().__init__()
#
#     def run(self):
#         threadTask(self.client)


def demo():
    fetchBaiduOCRClients()
    fetchClients()
    client = G_SHANGHAI_CLIENTS_DEBUG[0]
    for StartTime in client['StartTime'].split(', '):
        while True:
            Token = fetchToken(client, StartTime)
            # print(Token)
            while True:  # 死循环,直至验证码识别结果为4个数字为止
                captchaDict = downloadCaptcha(Token)
                CaptchaText = verificationCaptcha(captchaDict, 0)
                if CaptchaText:
                    break
            rText = submit(client, StartTime, Token, CaptchaText)
            if '预约成功' in rText:
                print(f'☺预约成功! [护照号码: {client["TraveldocumentNumber"]} 时间: {StartTime}]')
                return True
            elif '此时间已有其他预约' in rText:
                print(f'预约失败,此时间已有其他预约! [护照号码: {client["TraveldocumentNumber"]} 时间: {StartTime}]')
                return False
            elif '您已经有一个预约' in rText:
                print(f'恭喜!该客户已经成功预约了一个时间!不需要重复预约了! [护照号码: {client["TraveldocumentNumber"]}]')
                return False
            elif '您所输入的与图像中的文字不符' in rText:
                print('您所输入的与图像中的文字不符 重新抓取')
        break


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # """
    if not fetchBaiduOCRClients():
        print('获取OCR帐号失败!')
    elif not fetchClients():
        print('获取客户信息失败,请确认服务器已就绪!')
    else:
        print('开始预约')
        print(f'G_DEBUG: {G_DEBUG}')
        if not G_DEBUG:
            with ThreadPoolExecutor(
                    max_workers=len(G_PEKING_CLIENTS) + len(G_SHANGHAI_CLIENTS)) as executor:
                for client in G_PEKING_CLIENTS:
                    executor.submit(threadTask, (client))
                loopFetchAndSetUnknownCalendarId('SHANGHAI')  # 死循环直至上海(正式)面签机会的CalendarId出现
                for client in G_SHANGHAI_CLIENTS:
                    executor.submit(threadTask, (client))
        else:
            with ThreadPoolExecutor(
                    max_workers=len(G_PEKING_CLIENTS_DEBUG) + len(G_SHANGHAI_CLIENTS_DEBUG)) as executor:
                print(len(G_PEKING_CLIENTS_DEBUG) + len(G_SHANGHAI_CLIENTS_DEBUG))
                for client in G_PEKING_CLIENTS_DEBUG:
                    executor.submit(threadTask, (client))
                # loopFetchAndSetUnknownCalendarId(SHANGHAI)  # 死循环直至上海(正式)面签机会的CalendarId出现
                for client in G_SHANGHAI_CLIENTS_DEBUG:
                    executor.submit(threadTask, (client))

    # """
    # demo()
    """
    fetchBaiduOCRClients()
    fetchClients()
    startTime = G_SHANGHAI_CLIENTS_DEBUG[0]['StartTime'].split(' ')
    for s in startTime:
        startTimes = fetchStartTimes(G_SHANGHAI_CLIENTS_DEBUG[0], s)
        print(startTimes)
    """
    pass
