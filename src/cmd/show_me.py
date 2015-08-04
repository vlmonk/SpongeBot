# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from grab import Grab
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


def show_me_currency():
    """
    Парсим главную одного известного поисковика
    :return: текущие биржевые курсы доллара и евро, относительно рубля
    """
    g_usd = Grab()
    g_eur = Grab()

    # USD
    USD_URL = 'https://news.yandex.ru/quotes/2002.html'

    try:
        g_usd.go(USD_URL)
    except:
        return 'FAIL'

    resp = g_usd.doc.select('//tr[@class="quote__head"]')

    USD = {
        'date': resp.select('//td[@class="quote__date"]').text(),
        'value': resp.select('//td[@class="quote__value"]').text(),
        'change': resp.select('//td[@class="quote__change"]').text(),
    }

    # EURO
    EUR_URL = 'https://news.yandex.ru/quotes/2000.html'
    try:
        g_eur.go(EUR_URL)
    except:
        return 'FAIL'

    resp = g_eur.doc.select('//tr[@class="quote__head"]')

    EURO = {
        'date': resp.select('//td[@class="quote__date"]').text(),
        'value': resp.select('//td[@class="quote__value"]').text(),
        'change': resp.select('//td[@class="quote__change"]').text(),
    }

    return '[{usd_date}]\n' \
           'USD: {usd_val} ({usd_change})\n' \
           'EUR: {eur_val} ({eur_change})\n'.format(usd_date=USD['date'], usd_val=USD['value'],
                                                    usd_change=USD['change'],
                                                    eur_date=EURO['date'], eur_val=EURO['value'],
                                                    eur_change=EURO['change'])
