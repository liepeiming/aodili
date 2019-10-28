#!/usr/bin/env python3
import pathlib
import re
import time

import cv2
import numpy as np
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

requests.packages.urllib3.disable_warnings()

url = 'https://appointment.bmeia.gv.at'
ua = 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10'
Token_pattern = re.compile(r'<input id="Token" name="Token" type="hidden" value="(.*?)"')
ZhongLian_pattern = re.compile(r'"val":"(\d{4})"')


def dama(api_username, api_password, file_name, file_content, api_post_url, yzm_min, yzm_max, yzm_type, tools_token):
    '''
            main() 参数介绍
            api_username    （API账号）             --必须提供
            api_password    （API账号密码）         --必须提供
            file_name       （需要识别的图片路径）   --必须提供
            file_content       （需要识别的图片路径）   --必须提供
            api_post_url    （API接口地址）         --必须提供
            yzm_min         （识别结果最小长度值）        --可空提供
            yzm_max         （识别结果最大长度值）        --可空提供
            yzm_type        （识别类型）          --可空提供
            tools_token     （工具或软件token）     --可空提供
    '''
    # api_username =
    # api_password =
    # file_name = 'c:/temp/lianzhong_vcode.png'
    # api_post_url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"
    # yzm_min = '4'
    # yzm_max = '4'
    # yzm_type = '1038'
    # tools_token = api_username

    # proxies = {'http': 'http://127.0.0.1:8888'}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
        # 'Content-Type': 'multipart/form-data; boundary=---------------------------227973204131376',
        'Connection': 'keep-alive',
        'Host': 'v1-http-api.jsdama.com',
        'Upgrade-Insecure-Requests': '1'
    }

    files = {
        # 'upload': (file_name, open(file_name, 'rb'), 'image/png')
        'upload': (file_name, file_content, 'image/png')
    }

    data = {
        'user_name': api_username,
        'user_pw': api_password,
        'yzm_minlen': yzm_min,
        'yzm_maxlen': yzm_max,
        'yzmtype_mark': yzm_type,
        'zztool_token': tools_token
    }
    # s = requests.session()
    # r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False, proxies=proxies)
    # r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False)
    r = requests.post(api_post_url, headers=headers, data=data, files=files, verify=False)
    # print(r.text)
    return r.text


def fetch_CalendarId(session, payload):
    headers = {
        'User-Agent': ua,
        'Host': 'appointment.bmeia.gv.at',
        'Origin': 'https://appointment.bmeia.gv.at',
        'Referer': 'https://appointment.bmeia.gv.at/',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
    }
    data = {
        'Language': 'de',
        'Command': '下一步',
        'Office': payload['Office'],
    }
    CalendarId_pattern = re.compile(
        r'<option value="(.*?)">.*?%s.*?</option>' % payload['fuzzy_field'].replace('"', '&quot;'))

    while True:
        try:
            r = session.post(url, headers=headers, data=data, verify=False)
            # print(r.text)
            CalendarId = re.search(CalendarId_pattern, r.text)
            return CalendarId.group(1)
        except Exception as e:
            print(e)


def fetch_Token(session, payload):
    headers = {
        'User-Agent': ua,
        'Host': 'appointment.bmeia.gv.at',
        'Origin': 'https://appointment.bmeia.gv.at',
        'Referer': 'https://appointment.bmeia.gv.at/?fromSpecificInfo=True',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
    }
    data = {
        'Language': 'zh',
        'Office': payload['Office'],
        # 'CalendarId': '7226345',  # 这个是客户需要的选项,11月的时候才会用
        'CalendarId': payload['CalendarId'],
        'PersonCount': '1',
        'Monday': payload['Monday'],
        'Start': payload['Start'],
        'Command': '下一步',
    }
    while True:
        try:
            r = session.post(url + '/HomeWeb/Scheduler', headers=headers, data=data, verify=False)
            token = re.search(Token_pattern, r.text)
            return token.group(1)
        except Exception as e:
            print(e)


def download_captcha(session, token):
    headers = {
        'User-Agent': ua,
        'Cache-Control': 'no-cache',
        'Host': 'appointment.bmeia.gv.at',
        'Pragma': 'no-cache',
        'Referer': 'https://appointment.bmeia.gv.at/HomeWeb/Scheduler',
    }
    while True:
        try:
            r = session.get(url + '/Captcha?token=' + token, headers=headers, verify=False, stream=True)
            return r.content
        except Exception as e:
            print(e)


def distinguish(captcha_bytes: bytes) -> str:
    # 图片处理一下
    im_gray = cv2.imdecode(np.frombuffer(captcha_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
    ret, im_inv = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    captcha = cv2.morphologyEx(im_inv, cv2.MORPH_OPEN, kernel)
    gray_captcha_bytes = cv2.imencode('.png', captcha)[1]

    res = dama('liepeiming', 'lpm154az.', 'captcha', gray_captcha_bytes,
               "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload", '4', '4', '1009',
               'zUEJFiotBpA988Hjgsm4kfthjfhj6Detm4XdkcZW')
    if res:
        print(res)
        res = re.search(ZhongLian_pattern, res)
        if res:
            res = res.group(1)
            if len(res) == 4:
                captcha_text = res
                return captcha_text
    return False


def submit_form(session, payload) -> bool:
    headers = {
        'Accept-Encoding': "gzip, deflate, br",
        # 'Cookie': 'ASP.NET_SessionId=kks5vtmybrpnoyc0ety3sfbh',
        'Host': 'appointment.bmeia.gv.at',
        'Origin': 'https://appointment.bmeia.gv.at',
        'Referer': 'https://appointment.bmeia.gv.at/HomeWeb/Scheduler',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua,
    }
    data = {
        'Office': payload['Office'],
        'Language': 'zh,',
        'CalendarId': payload['CalendarId'],
        'Token': payload['Token'],
        'PersonCount': '1',
        'StartTime': payload['Start'],
        'Lastname': payload['Lastname'],
        'Firstname': payload['Firstname'],
        'DateOfBirth': payload['DateOfBirth'],
        'TraveldocumentNumber': payload['TraveldocumentNumber'],
        'Sex': payload['Sex'],
        'Street': payload['Street'],
        'Postcode': payload['Postcode'],
        'City': payload['City'],
        'Country': payload['Country'],
        'Telephone': payload['Telephone'],
        'Email': payload['Email'],
        'LastnameAtBirth': payload['LastnameAtBirth'],
        'NationalityAtBirth': payload['NationalityAtBirth'],
        'CountryOfBirth': payload['CountryOfBirth'],
        'PlaceOfBirth': payload['PlaceOfBirth'],
        'NationalityForApplication': payload['NationalityForApplication'],
        'TraveldocumentDateOfIssue': payload['TraveldocumentDateOfIssue'],
        'TraveldocumentValidUntil': payload['TraveldocumentValidUntil'],
        'TraveldocumentIssuingAuthority': payload['TraveldocumentIssuingAuthority'],
        'DSGVOAccepted': True,
        'CaptchaText': payload['CaptchaText'],
        'Command': '下一步',

    }
    r = session.post(url + '/HomeWeb/Appointment', data=data, headers=headers)
    if r.status_code == 200:
        with open(f'result_{int(time.time())}.html', 'w') as fp:
            fp.write(r.text)
        if '预约成功' in r.text:
            print('预约成功')
            return True
        elif '您所输入的与图像中的文字不符' in r.text:
            Token = fetch_Token(session, payload)
            print('Token: ', Token)
            captcha_bytes = download_captcha(session, Token)
            captcha_text = distinguish(captcha_bytes)
            if captcha_text:
                payload['CaptchaText'] = captcha_text
                return submit_form(session, payload)
        elif '以下信息没有输入或输入有误' in r.text:
            print('信息有误!请检查您输入的信息')
            return False


def task(payload) -> bool:
    session = requests.session()
    if payload.get('fuzzy_field'):
        CalendarId = fetch_CalendarId(session, payload)
        payload['CalendarId'] = CalendarId
    print('CalendarId: ', payload['CalendarId'])
    Token = fetch_Token(session, payload)
    payload['Token'] = Token
    print('Token: ', Token)
    captcha_bytes = download_captcha(session, Token)
    captcha_text = distinguish(captcha_bytes)
    if captcha_text:
        payload['CaptchaText'] = captcha_text
        return submit_form(session, payload)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    payload = {
        'Office': 'PEKING',

        # 'fuzzy_field': 'Chinesische',
        'CalendarId': '1213873',

        'Monday': '9/9/2019 0:00:00',
        'Start': '9/9/2019 10:00:00',

        'Firstname': 'Xue',
        'Lastname': 'Yue',
        'Firstname': 'HaiQiang',
        'DateOfBirth': '10.02.2010',
        'TraveldocumentNumber': 'EE4153518',
        'Sex': '2',  # Female: 2
        'Street': 'Huanghe 1Road,Qingdao',
        'Postcode': '266071',
        'City': 'Qingdao',
        'Country': '46',
        'Telephone': '13726254737',
        'Email': '714486244@qq.com',
        'LastnameAtBirth': 'Xue',
        'NationalityAtBirth': '49',
        'CountryOfBirth': '49',
        'PlaceOfBirth': 'Shandong',
        'NationalityForApplication': '49',
        'TraveldocumentDateOfIssue': '15.10.2018',
        'TraveldocumentValidUntil': '14.10.2023',
        'TraveldocumentIssuingAuthority': '49',
    }
    task(payload)
