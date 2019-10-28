#!/usr/bin/env python3
import random
import re
import json
import time
import queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import urllib
import requests
from bs4 import BeautifulSoup
import numpy as np
import cv2
from aip import AipOcr


SERV_URL = "http://127.0.0.1:8888"
BASE_URL = "https://appointment.bmeia.gv.at"


def fetchOffice() -> list:
    r = requests.get(BASE_URL)
    if r.status_code != 200:
        return False
    soup = BeautifulSoup(r.text, "lxml")
    officeSelect = soup.find("select", id="Office")
    if not officeSelect:
        return False
    options = officeSelect.find_all("option")
    options = options[1:]
    tmp = []
    for option in options:
        tmp.append(option.text)
    print(tmp)
    return tmp


def fetchCalendarId(offices: list or str = None) -> list:
    if isinstance(offices, str):
        offices = [offices]
    tmpAll = []
    for office in offices:
        r = requests.post(
            BASE_URL, data={"Language": "de", "Office": office, "Command": "下一步"}
        )
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
            CalendarIdSelect = soup.find("select", id="CalendarId")
            if CalendarIdSelect:
                options = CalendarIdSelect.find_all("option")
                options = options[1:]
                tmpOne = []
                for option in options:
                    tmpOne.append((option["value"], option.text))
                if tmpOne:
                    tmpAll.append({"office": office, "data": tmpOne})
    print(tmpAll)
    return tmpAll


def mp32wav(filepath):
    from pydub import AudioSegment

    song = AudioSegment.from_mp3(filepath)
    song.export("now.wav", format="wav")


def speechVerificationCodeRecognition(filepath: str) -> str:
    import speech_recognition as sr

    r = sr.Recognizer()
    demo = sr.AudioFile(filepath)
    with demo as source:
        audio = r.record(source, offset=0, duration=8)
    text = r.recognize_google(audio, language="en-US", show_all=True)
    print(text)


"""
def main():
    officeType = int(input('请输入您要预约的使领馆(0PEKING演示、1SHANGHAI演示、2PEKING、3SHANGHAI): '))
    if officeType:
        r = requests.get(SERV_URL + )
"""


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Offices = fetchOffice()
    # Offices = 'SHANGHAI'
    # CalendarIds = fetchCalendarId(Offices)
    speechVerificationCodeRecognition("now.wav")
    pass
