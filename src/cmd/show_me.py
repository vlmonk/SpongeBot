# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests

BOOBS_API = 'http://api.oboobs.ru/noise/1'
BOOBS_URL = 'http://media.oboobs.ru/'
BUTTS_API = 'http://api.obutts.ru/noise/1'
BUTTS_URL = 'http://media.obutts.ru/'


def show_me_boobs():
    """
    :return: ссылка на картинку с сиськами
    """
    try:
        request = requests.get(url=BOOBS_API)
    except:
        return False
    if not request.status_code == 200: return False
    url = request.json()[0]['preview']
    return BOOBS_URL + url


def show_me_butts():
    """
    :return: ссылка на картинку с жопой
    """
    try:
        request = requests.get(url=BUTTS_API)
    except:
        return False
    if not request.status_code == 200: return False
    url = request.json()[0]['preview']
    return BUTTS_URL + url


def show_me_turtle():
    """
    :return: ссылка на черепаху, похожую на Бурика
    """
    return 'https://mvl-private.s3.eu-central-1.amazonaws.com/files/4NLElhE.jpg'
