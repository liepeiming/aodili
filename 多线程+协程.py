#!/usr/bin/env python3
from gevent import monkey;

monkey.patch_all()
import gevent
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import urllib.request
import requests

BASE_URL = 'https://appointment.bmeia.gv.at'
G_GREENLETS = []


def run_task(url, num):
    print(f'Visit --> {url}, {num}')
    try:
        # response = urllib.request.urlopen(url)
        # data = response.read()
        response = requests.get(url)
        data = response.text
        print(f'{len(data)} bytes received from {url}.')
    except Exception as e:
        print(e)


def threadTask(urls):
    print('进程开始')
    global G_GREENLETS
    urls = [
        BASE_URL,
        'https://www.baidu.com',
        'https://docs.python.org/3/library/urllib.html',
        'https://www.weibo.com',
        'https://www.cnblogs.com/wangmo/p/7784867.html',
    ]
    num = 0
    greenlets = [gevent.spawn(run_task, url, num) for url in urls]
    gevent.joinall(greenlets)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    urls = [
        BASE_URL,
        'https://www.baidu.com',
        'https://docs.python.org/3/library/urllib.html',
        'https://www.weibo.com',
        'https://www.cnblogs.com/wangmo/p/7784867.html',
    ]
    # greenlets = [gevent.spawn(run_task, url, num) for url in urls]
    # gevent.joinall(greenlets)
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(threadTask, (urls))
        executor.submit(threadTask, (urls))
        executor.submit(threadTask, (urls))



    pass
