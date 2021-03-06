# -*- coding: utf-8 -*-
#
#   bot_d
#   =====
#   ver.: 2.1.0
#
#   «Я видел некоторое дерьмо»
#                       Букля.
#
#   @SpongeBot
#   ~~~~~~~~~~
#   Демон для работы с API бота для уютного чатика «/dev/null»
#   Умеет много всякого. И продолжает учиться. В отличии от тебя.
#
#   (с) @egregors 2015

from __future__ import unicode_literals

import logging
from time import sleep

import click
import requests
import telegram
from config import CHAT_ID, INTERVAL, TOKEN, DOCKER
from grab import Grab

try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError  # python 2

VERSION = 'ver.: 2.1.0'

if DOCKER:
    logging.basicConfig(level=logging.WARNING, filename='/var/log/sponge/bot.log')
else:
    logging.basicConfig(level=logging.WARNING)


@click.group()
def bot_d():
    """ Демон Бота
    :return:
    """
    pass


@click.group()
def bot_cli():
    """ CLI Бота
    :return:
    """
    pass


@bot_d.command()
def start():
    """ Start bot_d daemon """
    update_id = None
    bot = telegram.Bot(token=TOKEN)

    def send(msg: str, ch_id: int):
        bot.sendMessage(chat_id=ch_id, text=msg)

    def check_updates(b: telegram.Bot, update_id: int) -> int:

        for update in b.getUpdates(
                offset=update_id,
                timeout=INTERVAL,
        ):
            message = update.message.text
            upd_chat_id = update.message.chat_id
            update_id = update.update_id + 1
            cmd = message.lower()

            if upd_chat_id in CHAT_ID:
                # commands list

                if '/ping' in cmd:
                    send('Pong!', ch_id=upd_chat_id)

                elif 'сиськ' in cmd or '/boobs' in cmd:
                    bot.sendPhoto(chat_id=upd_chat_id, photo=get_boobs_url())

                elif 'жоп' in cmd or '/ass' in cmd:
                    bot.sendPhoto(chat_id=upd_chat_id, photo=get_butts_url())

                elif 'курс' in cmd or 'currency' in cmd:
                    send(msg=get_currency(), ch_id=upd_chat_id)

                elif '/ver' in cmd:
                    send(msg=VERSION, ch_id=upd_chat_id)

            else:
                pass

        return update_id

    while True:
        try:
            update_id = check_updates(bot, update_id)
        except telegram.TelegramError as e:
            # These are network problems with Telegram.
            if e.message in ("Bad Gateway", "Timed out", "Unauthorized"):
                sleep(1)
            else:
                raise e
        except URLError as e:
            # These are network problems on our end.
            sleep(1)


@bot_cli.command()
@click.option('-m', '--msg', help='Message to send', type=str)
@click.option('-c', '--chat_id', help='Chat ID', type=int)
def send(msg: str, chat_id: int):
    """ Send the message into Chat """
    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(chat_id=chat_id, text=msg)


# ================================================================= #
# AUX functions                                                     #
# ================================================================= #

BOOBS_API = 'http://api.oboobs.ru/noise/1'
BOOBS_URL = 'http://media.oboobs.ru/'
BUTTS_API = 'http://api.obutts.ru/noise/1'
BUTTS_URL = 'http://media.obutts.ru/'


def get_boobs_url():
    """
    :return: ссылка на картинку с сиськами
    """
    try:
        request = requests.get(url=BOOBS_API)
    except:
        return False
    if not request.status_code == 200: return False
    url = request.json()[0]['preview'].replace('_preview', '')
    return BOOBS_URL + url


def get_butts_url():
    """
    :return: ссылка на картинку с жопой
    """
    try:
        request = requests.get(url=BUTTS_API)
    except:
        return False
    if not request.status_code == 200: return False
    url = request.json()[0]['preview'].replace('_preview', '')
    return BUTTS_URL + url


def get_currency():
    """
    Парсим главную одного известного поисковика
    :return: текущие биржевые курсы доллара и евро, относительно рубля
    """
    g_usd = Grab()
    g_eur = Grab()
    g_cny = Grab()
    g_fuel = Grab()

    USD_URL = 'https://news.yandex.ru/quotes/2002.html'
    EUR_URL = 'https://news.yandex.ru/quotes/2000.html'
    CNY_URL = 'https://news.yandex.ru/quotes/10018.html'
    FUEL_URL = 'https://news.yandex.ru/quotes/1006.html'

    try:
        g_usd.go(USD_URL)
        g_eur.go(EUR_URL)
        g_cny.go(CNY_URL)
        g_fuel.go(FUEL_URL)
    except:
        return 'FAIL'

    resp = g_usd.doc.select('//tr[@class="quote__head"]')
    USD = {
        'date': resp.select('//td[@class="quote__date"]').text(),
        'value': resp.select('//td[@class="quote__value"]').text(),
        'change': resp.select('//td[@class="quote__change"]').text(),
    }

    resp = g_eur.doc.select('//tr[@class="quote__head"]')
    EURO = {
        'date': resp.select('//td[@class="quote__date"]').text(),
        'value': resp.select('//td[@class="quote__value"]').text(),
        'change': resp.select('//td[@class="quote__change"]').text(),
    }

    resp = g_cny.doc.select('//tr[@class="quote__head"]')
    CNY = {
        'date': resp.select('//td[@class="quote__date"]').text(),
        'value': resp.select('//td[@class="quote__value"]').text(),
        'change': resp.select('//td[@class="quote__change"]').text(),
    }

    resp = g_fuel.doc.select('//tr[@class="quote__head"]')
    FUEL = {
        'date': resp.select('//td[@class="quote__date"]').text(),
        'value': resp.select('//td[@class="quote__value"]').text(),
        'change': resp.select('//td[@class="quote__change"]').text(),
    }

    return 'USD: {usd_val} ({usd_change})\n' \
           'EUR: {eur_val} ({eur_change})\n' \
           'CNY: {cny_val} ({cny_change})\n' \
           '=================\n' \
           'Brent: {fuel_val} ({fuel_change})'.format(usd_val=USD['value'], usd_change=USD['change'],
                                                      eur_val=EURO['value'], eur_change=EURO['change'],
                                                      cny_val=CNY['value'], cny_change=CNY['change'],
                                                      fuel_val=FUEL['value'], fuel_change=FUEL['change'])


# ================================================================= #
# Main()                                                            #
# ================================================================= #

cli = click.CommandCollection(sources=[bot_d, bot_cli])

if __name__ == '__main__':
    cli()
