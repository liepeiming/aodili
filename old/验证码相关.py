#!/usr/bin/env python3
import os
import re
import json
import time
import cv2
import pytesseract
from PIL import Image
from aip import AipOcr
from qqai import ImgToText
import queue
import numpy as np
from matplotlib import pyplot as plt
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from qqai.vision.ocr import HandwritingOCR, GeneralOCR

requests.packages.urllib3.disable_warnings()

Q = queue.Queue(5)
TQ = queue.Queue(5)

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


def baidu_ocr(img_bytes):
    """百度OCR"""
    baidu_ocr_client = Q.get()
    res = baidu_ocr_client.numbers(img_bytes, baidu_ocr_options)
    Q.put(baidu_ocr_client)
    print(res)


def tx_ocr(fielanme):
    app_id = '2118496619'
    app_key = 'wkYirAby3uLpMsuA'
    # robot = HandwritingOCR(app_id=app_id, app_key=app_key)
    robot = GeneralOCR(app_id=app_id, app_key=app_key)
    """腾讯OCR"""
    with open(fielanme, 'rb') as fp:
        res = robot.run(fp)
    print(res)


def quzao():
    app_id = '2118496619'
    app_key = 'wkYirAby3uLpMsuA'
    robot = HandwritingOCR(app_id=app_id, app_key=app_key)
    for f in os.listdir('htmls/0'):
        img = cv2.imread(f'htmls/0/{f}')
        print(img.shape)
        time_start = time.time()
        nl = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        gray = cv2.cvtColor(nl, cv2.COLOR_RGB2GRAY)

        ret, im_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        captcha = cv2.morphologyEx(im_inv, cv2.MORPH_OPEN, kernel)
        # gray_captcha_bytes = cv2.imencode('.png', captcha)[1]

        # cv2.imwrite(f'htmls/1/{f}', gray)

        # cv2.imshow('img', img)
        # cv2.imshow('nl', nl)
        # cv2.imshow('gray', gray)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 字符分割可以采用 垂直投影

        img_encode = cv2.imencode('.png', captcha)[1]
        data_encode = np.array(img_encode)
        str_encode = data_encode.tostring()
        # cv2.imshow('img', img)
        # cv2.imshow('nl', nl)
        # cv2.imshow('captcha', captcha)
        # cv2.waitKey(0)
        """百度OCR
        baidu_ocr_client = Q.get()
        res = baidu_ocr_client.numbers(data_encode, baidu_ocr_options)
        Q.put(baidu_ocr_client)
        print(res)
        """
        """腾讯ocr"""
        with open('htmls/1/1563325810.png', 'rb') as fp:
            res = robot.run(fp)
        print(res)
        return False


def process():
    for f in os.listdir('./htmls/2'):
        img = cv2.imread(f'./htmls/2/{f}')
        """
        nl = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        gray = cv2.cvtColor(nl, cv2.COLOR_RGB2GRAY)

        ret, im_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        captcha = cv2.morphologyEx(im_inv, cv2.MORPH_OPEN, kernel)

        # img_encode = cv2.imencode('.png', captcha)[1]
        # data_encode = np.array(img_encode)
        # str_encode = data_encode.tostring()

        cv2.imwrite(f'./htmls/2/{f}', captcha)
        """
        with open(f'./htmls/2/{f}', 'rb') as fp:
            baidu_ocr(fp.read())
        time.sleep(2)


def naive_remove_noise(img_bytes, k):
    """
    8邻域降噪
    Args:
        # image_name: 图片文件命名
        image_obj: cv2
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
    gray_img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
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

    # return gray_img
    return cv2.imencode('.png', gray_img)[1]


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # tx_ocr('./htmls/1/1563325810.png')
    # with open('./htmls/1/1563325810.png', 'rb') as fp:
    #     img_bytes = fp.read()
    #     baidu_ocr(img_bytes)
    # quzao()
    for f in os.listdir('./htmls/0'):
        # res = pytesseract.image_to_string(Image.open(f'./htmls/2/{f}'))
        # print(res)
        with open(f'./htmls/0/{f}', 'rb') as fp:
            img = naive_remove_noise(fp.read(), 4)
        with open(f'./htmls/gray_captcha.png', 'wb') as fp:
            fp.write(img)
        baidu_ocr(img)
        break
