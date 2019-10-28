#!/usr/bin/env python3
# import os
import random
import re
# import json
import time
import cv2
from aip import AipOcr
# from qqai import ImgToText
import queue
import numpy as np
# from matplotlib import pyplot as plt
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor

# from qqai.vision.ocr import HandwritingOCR

requests.packages.urllib3.disable_warnings()

DEBUG = False
TEST = True

url = 'https://appointment.bmeia.gv.at'
ua = 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10'
Token_pattern = re.compile(r'<input id="Token" name="Token" type="hidden" value="(.*?)"')
ZhongLian_pattern = re.compile(r'"val":"(\d{4})"')
# Monday_list = []
# StartTime_list = []

Monday_StartTime_table = []
ORDER_NUMBER = 0

Q = queue.Queue()
# TQ = queue.Queue()

baidu_ocr_options = {}
baidu_ocr_options["recognize_granularity"] = "small"
baidu_ocr_options["detect_direction"] = "true"

# ------------------------------------------------------------
APP_ID = '16232754'
API_KEY = '6peGW76zeFyRB9QmYUdDBRrW'
SECRET_KEY = '1VXMjpITrniaXMp9tTkqHOmdVgiBcd1S'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16667240'
API_KEY = 'kGdWqRmYqCvMMAtwRmyi3gcr'
SECRET_KEY = 'kUx6tQ699OGf27SLvWkPxpWYbEUjpaxF'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16667411'
API_KEY = 'MO31imWKDp5uD4blCoelC3SG'
SECRET_KEY = 'XEftlFpcxDmD0NM4DPICiun0ydBTYHPy'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16667478'
API_KEY = 'dyrn8EIcBa97q3gSjQS3SpT7'
SECRET_KEY = '5Cs6fReXyF8jeEjcquWx4R3vyZlTwtK7'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16668509'
API_KEY = 'hTIi04vTlR6ka0kdD7CLveL0'
SECRET_KEY = 'TOfS1mVAt7SeizseffqAZpKBPnWuOAoV'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16850942'
API_KEY = 'QmDoi0uNCNycHjGl7xpAjIY3'
SECRET_KEY = 'E6Qm7YFbMNsVvIxNql0SU7VbKXLm1ovc'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16850943'
API_KEY = 'rCe4ZXDuegUaCqCPIT1s9zTK'
SECRET_KEY = 'R08Khxcrz4Ox66PGOQVNke7HY9snBiTz'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16850944'
API_KEY = 'xuPzEQsjgbKn4mezV0DLVvcC'
SECRET_KEY = 'SYO30yjpADFRdlM3596GKakrUlPifDQo'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16850945'
API_KEY = 'rLFDYB8uoLnPr5UqPZBSCaVl'
SECRET_KEY = 'bcUgs2V9HnPNWqB6rIZojHDvg4rK8TxQ'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16850946'
API_KEY = 'vlGEIZXImmwYb3fjHC3VkC7Q'
SECRET_KEY = 'LOZ8Si11rMDMrrPW2Oony7wpsFAcaRFA'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16850948'
API_KEY = 'T9k37200VOVUZzbw2nHT2Qb6'
SECRET_KEY = 'ld0Gk5dA4UvHlV5gU9GOZRM0y27ScgZx'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16850949'
API_KEY = 'db2lq5quwtVwuVthK7t5dE2Y'
SECRET_KEY = 'GGtqtbpvNj2zoMSaomiXLhj1O4LHNtQE'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16850950'
API_KEY = 'oxHOlryYwx0wMUKEDij49ma3'
SECRET_KEY = 'zrzFd0aOZGgOQDKEZIgs1O9esGSkFWhW'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16850951'
API_KEY = '200r3TiG24dK8PDO60Mi5LCl'
SECRET_KEY = 'nkI8pNQG8nGG6DiiBX5yrPk1zQKF61x8'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)
# ------------------------------------------------------------
APP_ID = '16850953'
API_KEY = 'sMTbLUC5IFkNzG4s7nH7zHEI'
SECRET_KEY = 'Qz4oU0xYy9hl5vVGgGpuCPDL1vCnh0Qa'
baidu_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
Q.put(baidu_ocr_client)


class Client(object):
    def __init__(self, Firstname, Lastname, DateOfBirth, TraveldocumentNumber, Sex, Street, Postcode, City,
                 Telephone, Email, LastnameAtBirth, PlaceOfBirth, NationalityForApplication, TraveldocumentDateOfIssue,
                 TraveldocumentValidUntil, Country='46', CountryOfBirth='49', NationalityAtBirth='49',
                 TraveldocumentIssuingAuthority='49'):
        self.Firstname = Firstname
        self.Lastname = Lastname
        self.DateOfBirth = DateOfBirth
        self.TraveldocumentNumber = TraveldocumentNumber
        if '男' in Sex or Sex == 'Male' or Sex == 'male' or Sex == '1' or Sex == 1:
            self.Sex = '1'
        else:
            self.Sex = '2'
        self.Street = Street
        self.Postcode = Postcode
        self.City = City
        self.Country = Country
        self.Telephone = Telephone
        self.Email = Email
        self.LastnameAtBirth = LastnameAtBirth
        self.NationalityAtBirth = NationalityAtBirth
        self.CountryOfBirth = CountryOfBirth
        self.PlaceOfBirth = PlaceOfBirth
        self.NationalityForApplication = NationalityForApplication
        self.TraveldocumentDateOfIssue = TraveldocumentDateOfIssue
        self.TraveldocumentValidUntil = TraveldocumentValidUntil
        self.TraveldocumentIssuingAuthority = TraveldocumentIssuingAuthority

    def to_dict(self):
        return {
            'Firstname': self.Firstname,
            'Lastname': self.Lastname,
            'DateOfBirth': self.DateOfBirth,
            'TraveldocumentNumber': self.TraveldocumentNumber,
            'Sex': self.Sex,
            'Street': self.Street,
            'Postcode': self.Postcode,
            'City': self.City,
            'Country': self.Country,
            'Telephone': self.Telephone,
            'Email': self.Email,
            'LastnameAtBirth': self.LastnameAtBirth,
            'NationalityAtBirth': self.NationalityAtBirth,
            'CountryOfBirth': self.CountryOfBirth,
            'PlaceOfBirth': self.PlaceOfBirth,
            'NationalityForApplication': self.NationalityForApplication,
            'TraveldocumentDateOfIssue': self.TraveldocumentDateOfIssue,
            'TraveldocumentValidUntil': self.TraveldocumentValidUntil,
            'TraveldocumentIssuingAuthority': self.TraveldocumentIssuingAuthority,
        }


class Order(object):
    def __init__(self, Monday, Start, client, Office=None, fuzzy_field=None, CalendarId=None):
        self.Office = Office
        self.Monday = Monday
        self.Start = Start
        self.StartTime = Start
        self.client = client
        self.CalendarId = CalendarId
        if CalendarId:
            self.CalendarId = CalendarId
            self.fuzzy_field = None
        else:
            self.fuzzy_field = fuzzy_field
        self.Token = None
        self.CaptchaText = None

        # 下面这几个字段是不添加到to_dict()里的
        self.session = requests.session()
        self.captcha_bytes = None

    def to_dict(self):
        tmp_dict = self.client.to_dict()
        tmp_dict['Office'] = self.Office
        tmp_dict['Monday'] = self.Monday
        tmp_dict['Start'] = self.Start
        tmp_dict['StartTime'] = self.StartTime

        tmp_dict['PersonCount'] = '1'
        tmp_dict['Language'] = 'zh'
        tmp_dict['DSGVOAccepted'] = 'true'
        tmp_dict['Command'] = '下一步'

        tmp_dict['Token'] = self.Token
        tmp_dict['CalendarId'] = self.CalendarId
        tmp_dict['CaptchaText'] = self.CaptchaText

        return tmp_dict


def fetch_CalendarId(order):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'ASP.NET_SessionId=uivlt5blhlb5c2soci1b02z4',
        'DNT': '1',
        'Host': 'appointment.bmeia.gv.at',
        'Origin': 'https://appointment.bmeia.gv.at',
        'Referer': 'https://appointment.bmeia.gv.at/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua,
    }
    """
    data = {
        # 'Language': 'de',
        'Language': 'zh',
        'Office': order.Office,
        'Command': '下一步',
    }
    """
    data = order.to_dict()
    CalendarId_pattern = re.compile(
        r'<option value="(.*?)">.*?%s.*?</option>' % order.fuzzy_field.replace('"', '&quot;'))

    while True:
        try:
            r = order.session.post(url, headers=headers, data=data, verify=False)
            if r.status_code == 200:
                text = r.text
                if DEBUG:
                    with open('htmls/fetch_CalendarId.html', 'w', encoding='utf-8') as fp:
                        fp.write(text)
                search_result = re.search(CalendarId_pattern, text)
                if search_result:
                    CalendarId = search_result.group(1)
                    order.CalendarId = CalendarId
                    if DEBUG:
                        print('CalendarId: ', CalendarId)
                    return CalendarId
                print('没找到CalendarId')
        except Exception as e:
            print(e)


def fetch_StartTime():
    StartTime_pattern = re.compile(r'name="Start" type="radio" value="(.*?)" />')
    Monday_pattern = re.compile(r'周 (.*?) -')
    headers = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '94',
        # 'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'ASP.NET_SessionId=uivlt5blhlb5c2soci1b02z4',
        # 'DNT': '1',
        'Host': 'appointment.bmeia.gv.at',
        'Origin': 'https://appointment.bmeia.gv.at',
        'Referer': 'https://appointment.bmeia.gv.at/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua,
    }
    data = {
        'Language': 'zh',
        'Office': Office,
        'CalendarId': CalendarId,
        'PersonCount': '1',
        'Command': '下一步',
    }
    # data = order.to_dict()

    fetch_StartTime_url = url + '/?fromSpecificInfo=True'
    while True:
        r = requests.post(fetch_StartTime_url, headers=headers, data=data, verify=False)
        if r.status_code == 200:
            text = r.text
            if DEBUG:
                with open('htmls/fetch_DateTime.html', 'w', encoding='utf-8') as fp:
                    fp.write(text)
            find_result = StartTime_pattern.findall(text)
            monday_search_result = Monday_pattern.search(text)
            if find_result:
                global Monday_StartTime_table
                Monday = find_result[0].split(' ')[0] + ' 0:00:00'
                for StartTime in find_result:
                    Monday_StartTime_table.append({Monday: StartTime})
                # if len(Monday_StartTime_table) >= ORDER_NUMBER:
                #     return True
                if monday_search_result and '下一周' in text:
                    data['Command'] = '下一周'
                    data['Monday'] = monday_search_result.group(1) + ' 0:00:00'
                    headers['Referer'] = 'https://appointment.bmeia.gv.at/HomeWeb/Scheduler'
                    fetch_StartTime_url = 'https://appointment.bmeia.gv.at/HomeWeb/Scheduler'
                else:
                    return True
            else:
                return True
            if '下一周' not in text:
                return True


def fetch_Token(order):
    headers = {
        'User-Agent': ua,
        'Host': 'appointment.bmeia.gv.at',
        'Origin': 'https://appointment.bmeia.gv.at',
        'Referer': 'https://appointment.bmeia.gv.at/?fromSpecificInfo=True',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
    }
    """
    data = {
        'Language': 'zh',
        'Office': order.Office,
        # 'CalendarId': '7226345',  # 这个是客户需要的选项,11月的时候才会用
        'CalendarId': order.CalendarId,
        'PersonCount': '1',
        'Monday': order.Monday,
        'Start': order.Start,
        'Command': '下一步',
    }
    """
    data = order.to_dict()
    while True:
        try:
            r = order.session.post(url + '/HomeWeb/Scheduler', headers=headers, data=data, verify=False)
            if r.status_code == 200:
                text = r.text
                if DEBUG:
                    with open('htmls/fetch_Token.html', 'w', encoding='utf-8') as fp:
                        fp.write(text)
                search_result = re.search(Token_pattern, r.text)
                if search_result:
                    Token = search_result.group(1)
                    # 记住是在这里设置order的Token
                    order.Token = Token
                    if DEBUG:
                        print('Token: ', Token)
                    return Token
                print('没找到Token')
        except Exception as e:
            print(e)


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


def download_png_captcha(order):
    headers = {
        'User-Agent': ua,
        'Cache-Control': 'no-cache',
        'Host': 'appointment.bmeia.gv.at',
        'Pragma': 'no-cache',
        'Referer': 'https://appointment.bmeia.gv.at/HomeWeb/Scheduler',
    }
    while True:
        try:
            r = order.session.get(url + '/Captcha?token=' + order.Token, headers=headers, stream=True, verify=False)
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
                order.captcha_bytes = gray_content
                if DEBUG:
                    with open('htmls/origin_captcha.png', 'wb') as fp:
                        fp.write(content)
                    with open('htmls/gray_captcha.png', 'wb') as fp:
                        fp.write(gray_content)
                return gray_content
        except Exception as e:
            print(e)


def download_mp3_captcha(order):
    headers = {
        'Accept-Encoding': 'identity;q=1, *;q=0',
        'User-Agent': ua,
        'Range': 'bytes=0-',
        'Referer': 'https://appointment.bmeia.gv.at/HomeWeb/Scheduler',
    }
    while True:
        try:
            r = order.session.get(url + '/Captcha/Audio?token=' + order.Token + '&language=zh', headers=headers,
                                  stream=True, verify=False)
            if r.status_code == 200:
                content = r.content
                if DEBUG:
                    with open('htmls/Audio.mp3', 'wb') as fp:
                        fp.write(content)
                return content
        except Exception as e:
            print(e)


def baidu_ocr(img_bytes):
    baidu_ocr_client = Q.get()
    res = baidu_ocr_client.numbers(img_bytes, baidu_ocr_options)
    if DEBUG:
        print(res)
    Q.put(baidu_ocr_client)
    # res = json.loads(res)
    words_result = res.get('words_result')
    if words_result:
        words = words_result[0].get('words')
        if words and len(words) == 4:
            return words
    return None


def distinguish(order):
    """
    img = cv2.imdecode(np.frombuffer(captcha_bytes, np.uint8))
    nl = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
    gray = cv2.cvtColor(nl, cv2.COLOR_RGB2GRAY)
    """

    try:
        CaptchaText = baidu_ocr(order.captcha_bytes)
        order.CaptchaText = CaptchaText
        if DEBUG:
            print('CaptchaText: ', CaptchaText)
    except Exception as e:
        print(e)


def submit_form(order):
    headers = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '1239',
        # 'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'ASP.NET_SessionId=oiwrofkvymi1os0ybaqk1tyy',
        'Host': 'appointment.bmeia.gv.at',
        'Origin': 'https://appointment.bmeia.gv.at',
        'Pragma': 'no-cache',
        'Referer': 'https://appointment.bmeia.gv.at/HomeWeb/Scheduler',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua,
    }
    """
    data = {
        'Office': Office,
        'Language': 'zh',
        'CalendarId': CalendarId,
        'Token': Token,
        'PersonCount': '1',
        'StartTime': StartTime,
        'Lastname': Lastname,
        'Firstname': Firstname,
        'DateOfBirth': DateOfBirth,
        'TraveldocumentNumber': TraveldocumentNumber,
        'Sex': Sex,
        'Street': Street,
        'Postcode': Postcode,
        'City': City,
        'Country': Country,
        'Telephone': Telephone,
        'Email': Email,
        'LastnameAtBirth': LastnameAtBirth,
        'NationalityAtBirth': NationalityAtBirth,
        'CountryOfBirth': CountryOfBirth,
        'PlaceOfBirth': PlaceOfBirth,
        'NationalityForApplication': NationalityForApplication,
        'TraveldocumentDateOfIssue': TraveldocumentDateOfIssue,
        'TraveldocumentValidUntil': TraveldocumentValidUntil,
        'TraveldocumentIssuingAuthority': TraveldocumentIssuingAuthority,
        'DSGVOAccepted': 'true',
        'CaptchaText': CaptchaText,
        'Command': '下一步',
    }
    """

    i = 0
    while True:
        try:
            data = order.to_dict()
            """
            # 这里是模拟一次验证码识别失败的
            if DEBUG:
                if i == 0:
                    data['CaptchaText'] = '9527'
                    i += 1
            """
            r = order.session.post(url + '/HomeWeb/Appointment', headers=headers, data=data, verify=False)
            if DEBUG:
                print(data)
            if r.status_code == 200:
                text = r.text
                if DEBUG:
                    with open('htmls/submit_form.html', 'w', encoding='utf-8') as fp:
                        fp.write(text)
                if '预约成功' in text:
                    print('预约成功 ----------------------------------------------------')
                    return True
                elif '此时间已有其他预约' in text:
                    # 有其他预约,就换剩下的时间
                    if len(Monday_StartTime_table):
                        print('此时间已有其他预约, 换别的时间')
                        MST = Monday_StartTime_table.pop(0)
                        order.StartTime = list(MST.values())[0]
                        continue
                    else:
                        print('此时间已有其他预约, 这个星期都被抢完了!')
                        return False
                elif '您所输入的与图像中的文字不符' in text:
                    print('验证码有误')
                    # TODO: 从 text 中分析出Token,下载验证码,识别验证码,修改 data 中的 Token 和 CaptchaText,最后continue
                    search_res = re.search(Token_pattern, text)
                    if search_res:
                        Token = search_res.group(1)
                        order.Token = Token
                        if DEBUG:
                            print('Token: ', Token)
                        download_png_captcha(order)
                        distinguish(order)
                    continue
                elif '以下信息没有输入或输入有误' in text:
                    print('预约失败,表单信息有误!')
                    return False
        except Exception as e:
            print(e)


def task(index, order):
    if order.fuzzy_field:
        fetch_CalendarId(order)
    fetch_Token(order)
    download_png_captcha(order)
    distinguish(order)
    submit_form(order)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    Office = 'PEKING'
    CalendarId = '1213873'
    # CalendarId = '1213936'
    email = input('请输入您的邮箱地址: ')
    # ORDER_NUMBER = int(input('请输入您要抢多少个: '))
    fetch_StartTime()
    for _ in Monday_StartTime_table:
        print(_)
    _day = input('请输入您要预约哪一天(格式为 日/月/年): ')
    _Monday_StartTime_table = []
    for k in Monday_StartTime_table:
        start_time = list(k.values())[0]
        if _day in start_time:
            print(start_time)
            # Monday_StartTime_table.remove(k)
            _Monday_StartTime_table.append(k)
    ORDER_NUMBER = (int(input('请输入你要抢多少个(输入0表示全部): ')))
    if ORDER_NUMBER == 0 or ORDER_NUMBER >= len(_Monday_StartTime_table):
        ORDER_NUMBER = len(_Monday_StartTime_table)
    orders = []
    r = requests.get('http://localhost:8888/customer_information')
    if r.status_code == 200:
        clients = r.json()
        print(clients)
    """
    for i in range(ORDER_NUMBER):
        client = Client(
            Firstname='Dong',
            Lastname='Jiang',
            DateOfBirth='15/3/2016',
            # TraveldocumentNumber='EE4153511',  # FIXME: 这个字段要时刻改
            TraveldocumentNumber='EE41%d' % random.randint(10000, 99999),
            Sex='2',
            Street='Huanghe 1Road,Qingdao',
            Postcode='266071',
            City='Qingdao',
            Country='46',
            Telephone='13726254737',
            Email=email,
            LastnameAtBirth='Dong',
            NationalityAtBirth='49',
            CountryOfBirth='49',
            PlaceOfBirth='Shandong',
            NationalityForApplication='49',
            TraveldocumentDateOfIssue='15.10.2018',
            TraveldocumentValidUntil='14.10.2023',
            TraveldocumentIssuingAuthority='49',
        )
        """
    for c in clients:
        client = Client(
            Firstname=c['Firstname'],
            Lastname=c['Lastname'],
            DateOfBirth=c['DateOfBirth'],
            TraveldocumentNumber=c['TraveldocumentNumber'],
            Sex=c['Sex'],
            Street=c['Street'],
            Postcode=c['Postcode'],
            City=c['City'],
            Country=c['Country'],
            Telephone=c['Telephone'],
            Email=c['Email'],
            LastnameAtBirth=c['LastnameAtBirth'],
            NationalityAtBirth=c['NationalityAtBirth'],
            CountryOfBirth=c['CountryOfBirth'],
            PlaceOfBirth=c['PlaceOfBirth'],
            NationalityForApplication=c['NationalityForApplication'],
            TraveldocumentDateOfIssue=c['TraveldocumentDateOfIssue'],
            TraveldocumentValidUntil=c['TraveldocumentValidUntil'],
            TraveldocumentIssuingAuthority=c['TraveldocumentIssuingAuthority'],
        )
        Monday_StartTime = _Monday_StartTime_table.pop(0)
        orders.append(Order(
            Monday=list(Monday_StartTime.keys())[0],
            Start=list(Monday_StartTime.values())[0],
            client=client,
            Office=Office,
            CalendarId=CalendarId,
            fuzzy_field='Chinesische',
            # fuzzy_field='Mongolische',
        ))
    # ----------------------------------------------
    # with ProcessPollExecutor(max_workers=ORDER_NUMBER) as executor:
    with ThreadPoolExecutor(max_workers=ORDER_NUMBER) as executor:
        input('输入回车键开始抢单: ')
        threads = []
        for index, order in enumerate(orders):
            threads.append(executor.submit(task, (index), (order)))
        time_start = time.time()
        for res in as_completed(threads):
            # print(res.result())
            pass

    time_end = time.time()
    print('time cost', time_end - time_start, 's')
    input('输入回车键退出程序: ')
