#!/usr/bin/env python3
import re
import requests

requests.packages.urllib3.disable_warnings()

import aiohttp
import asyncio
import aiofiles
import async_timeout

url = 'https://appointment.bmeia.gv.at'
ua = 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10'
Token_pattern = re.compile(r'<input id="Token" name="Token" type="hidden" value="(.*?)"')


async def fetch_CalendarId(session, payload):
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
    CalendarId_pattern = re.compile(r'<option value="(.*?)">.*?%s.*?</option>' % payload['fuzzy_field'])

    while True:
        try:
            async with session.post(url, headers=headers, data=data, verify_ssl=False) as response:
                r = await response.text()
                # print(r)
                CalendarId = re.search(CalendarId_pattern, r)
                return CalendarId.group(1)
        except Exception as e:
            print(e)


async def fetch_Token(session, payload):
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
            async with session.post(url + '/HomeWeb/Scheduler', headers=headers, data=data,
                                    verify_ssl=False) as response:
                r = await response.text()
                token = re.search(Token_pattern, r)
                return token.group(1)
        except Exception as e:
            print(e)


async def download_captcha(session, token):
    headers = {
        'User-Agent': ua,
        'Cache-Control': 'no-cache',
        'Host': 'appointment.bmeia.gv.at',
        'Pragma': 'no-cache',
        'Referer': 'https://appointment.bmeia.gv.at/HomeWeb/Scheduler',
    }
    while True:
        try:
            async with session.get(url + '/Captcha?token=' + token, headers=headers, verify_ssl=False) as response:
                return response.content
        except Exception as e:
            print(e)


async def distinguish(img_bytes):
    pass


async def submit_form(session, payload):
    pass


async def main(loop, payload):
    async with aiohttp.ClientSession(loop=loop) as session:
        if 'fuzzy_field' in payload.keys():
            CalendarId = await fetch_CalendarId(session, payload)
        payload['CalendarId'] = CalendarId
        print('CalendarId: ', payload['CalendarId'])
        Token = await fetch_Token(session, payload)
        print('Token: ', Token)
        captcha_bytes = download_captcha(session, Token)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    payload = {
        'Office': 'PEKING',

        'fuzzy_field': 'Chinesische',

        'Monday': '5/8/2019 0:00:00',
        'Start': '6/8/2019 10:40:00',

        'Lastname': 'Liu',
        'Firstname': 'Xing',
        'DateOfBirth': '10.02.2010',
        'TraveldocumentNumber': 'EE4153522',
        'Sex': '2',  # Female: 2
        'Street': 'Huanghe 1Road,Qingdao',
        'Postcode': '266071',
        'City': 'Qingdao',
        'Country': '46',
        'Telephone': '13726254737',
        'Email': '714486244@qq.com',
        'LastnameAtBirth': 'Liu',
        'NationalityAtBirth': '49',
        'CountryOfBirth': '49',
        'PlaceOfBirth': 'Shandong',
        'NationalityForApplication': '49',
        'TraveldocumentDateOfIssue': '15.10.2018',
        'TraveldocumentValidUntil': '14.10.2023',
        'TraveldocumentIssuingAuthority': '49',
    }
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, payload))
