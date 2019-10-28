#!/usr/bin/env python3
import sys
from PyQt5.QtGui import QPixmap, QIntValidator, QFont, QIcon, QImage
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QHBoxLayout, QLineEdit, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QRect, QThread, QMutex

import random
import re
import queue
import requests

requests.packages.urllib3.disable_warnings()
url = 'https://appointment.bmeia.gv.at'
ua = 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10'
Token_pattern = re.compile(r'<input id="Token" name="Token" type="hidden" value="(.*?)"')
mutex = QMutex()


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


def distinguish(captcha_bytes):
    pass


def submit_form(session, payload) -> bool:
    return True


def task(qthreadId, payload, app):
    print('task')
    session = requests.session()
    # if 'fuzzy_field' in payload.keys():
    if payload.get('fuzzy_field'):
        CalendarId = fetch_CalendarId(session, payload)
        payload['CalendarId'] = CalendarId
        print('CalendarId: ', payload['CalendarId'])
        Token = fetch_Token(session, payload)
        print('Token: ', Token)
        captcha_bytes = download_captcha(session, Token)
        app.captchas[str(qthreadId)] = {
            'captcha_bytes': captcha_bytes,
            'captcha_text': None,
        }
        while True:
            captcha_text = app.captchas[str(qthreadId)].get('captcha_text')
            if captcha_text:
                mutex.lock()
                del app.captchas[app.current_task_thread]
                mutex.unlock()
                payload['CaptchaText'] = captcha_text
                res = submit_form(session, payload)
                if res:
                    app.success += 1
                else:
                    app.success += 1
                return res


class TaskThread(QThread):

    def __init__(self, payload, app):
        super(TaskThread, self).__init__()
        self.payload = payload
        self.app = app

    def run(self):
        print('TaskThread')
        task(self.currentThreadId(), self.payload, self.app)
        self.app.set_title()


class WaitCaptchaThread(QThread):
    def __init__(self, app):
        super(WaitCaptchaThread, self).__init__()
        self.app = app

    def run(self):
        print('WaitCaptchaThread')
        flag = False
        while True:
            if flag:
                break
            for k, v in self.app.captchas.items():
                captcha_bytes = v.get('captcha_bytes')
                if captcha_bytes:
                    mutex.lock()
                    # self.app.img.setPixmap(QPixmap.loadFromData(captcha_bytes))
                    self.app.captcha.loadFromData(captcha_bytes)
                    self.app.img.setPixmap(QPixmap.fromImage(self.app.captcha))
                    self.app.current_task_thread = k
                    mutex.unlock()
                    flag = True


class App(QWidget):

    def __init__(self, payloads):
        super().__init__()
        self.title = '奥地利共和国预约系统抢单软件'
        self.icon = 'favicon.ico'
        self.left = 450
        self.top = 250
        self.width = 640
        self.height = 480
        self.payloads = payloads
        self.task_threads = []
        self.current_task_thread = None
        self.captchas = {}
        self.success = 0
        self.failed = 0
        self.initUI()

    def set_title(self):
        self.setWindowTitle('%s 总:%d 成功:%d 失败:%d' % (self.title, len(self.payloads), self.success, self.failed))

    def initUI(self):
        self.set_title()
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon(self.icon))

        vbox = QVBoxLayout(self)

        self.img = QLabel(self)
        self.captcha = QImage()

        # self.captcha.loadFromData(self.first_img)
        # self.img.setPixmap(QPixmap('1.png'))  # 在label上显示图片 # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        # self.img.setPixmap(QPixmap.fromImage(self.captcha))
        self.img.setScaledContents(True)  # 让图片自适应label大小
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setValidator(QIntValidator(0000, 9999));
        # self.lineEdit.setPlaceholderText('请以最快速度打码')
        self.lineEdit.setFont(QFont('Timers', 34, QFont.Bold))

        self.wait_captcha_thread = WaitCaptchaThread(self)
        self.wait_captcha_thread.start()
        for payload in self.payloads:
            task_thread = TaskThread(payload, self)
            task_thread.start()
            self.task_threads.append(task_thread)

        vbox.addWidget(self.img)
        vbox.addWidget(self.lineEdit)
        self.setLayout(vbox)

        self.show()

    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key_Escape:
            self.lineEdit.clear()
        elif k == Qt.Key_Return or k == Qt.Key_Enter:
            if len(self.lineEdit.text()) == 4:
                if self.current_task_thread:
                    # FIXME: File "task.py", line 217, in keyPressEvent  KeyError: '<sip.voidptr object at 0x0000, 可能是task_thread中已经删除了那个...
                    self.captchas[self.current_task_thread]['captcha_text'] = self.lineEdit.text()
                    captcha_bytes = self.captchas[self.current_task_thread].get('captcha_bytes')
                    if captcha_bytes:
                        self.captcha.loadFromData(captcha_bytes)
                    self.img.setPixmap(QPixmap.fromImage(self.captcha))
                    # self.img.setPixmap(QPixmap.loadFromData(self.captchas[self.current_task_thread].get('captcha_bytes')))
                    # del self.captchas[self.current_task_thread]  # 这个在task_thread中删除
                    if len(self.captchas):
                        self.current_task_thread = list(self.captchas.keys())[0]
                    else:
                        self.current_task_thread = None
                self.lineEdit.clear()


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
    payloads = []
    payloads.append(payload)
    payloads.append(payload)

    app = QApplication(sys.argv)
    ex = App(payloads)
    sys.exit(app.exec_())
