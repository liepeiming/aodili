#!/usr/bin/env python3
import re

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import time
import cv2
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
CAPTCHA_PATH = './验证码/'
BASE_URL = 'https://appointment.bmeia.gv.at'
tokenPattern = re.compile(r'<input id="Token" name="Token" type="hidden" value="(.*?)"')


def fetchToken():
    r = requests.post(BASE_URL + '/HomeWeb/Scheduler', data={
        'Language': 'zh',
        'Office': 'BAKU',
        'CalendarId': '5539799',
        'PersonCount': '1',
        'Monday': '07.10.2019 00:00:00',
        'Start': '10.10.2019 09:15:00',
        'Command': '下一步',
    }, verify=False)
    if r.status_code == 200:
        # soup = BeautifulSoup(r.text, 'lxml')
        # captcha = soup.find(name='img', attrs={"class": "captcha"})
        # token = captcha['src'][15:]
        searchResult = re.search(tokenPattern, r.text)
        if searchResult:
            token = searchResult.group(1)
            return token


def downloadCaptcha(token, i):
    r = requests.get(BASE_URL + '/Captcha?token=' + token, stream=True, verify=False)
    if r.status_code == 200:
        with open(f'{CAPTCHA_PATH}{i}/{int(time.time())}.png', 'wb') as fp:
            fp.write(r.content)
            return True
    else:
        print('请求验证码失败', i)


def main(i):
    for _ in range(2500):
        token = fetchToken()
        # print(token)
        if token:
            if downloadCaptcha(token, i):
                print(f'线程{i}下载第{_}张验证码成功!')
            else:
                print(f'线程{i}下载第{_}张验证码失败!')
        else:
            print('获取token失败', i)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.submit(main, (1))
        executor.submit(main, (2))
        executor.submit(main, (3))
        executor.submit(main, (4))
    pass
