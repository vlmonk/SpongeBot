# -*- coding: utf-8 -*-
#
#   bot_d
#   =====
#   ver.: 2.0.1
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

import click
import requests
import telegram
from config import CHAT_ID, INTERVAL, TOKEN, DOCKER
from grab import Grab

VERSION = 'ver.: 2.0.2'

if DOCKER:
    logging.basicConfig(level=logging.WARNING, filename='/var/log/sponge/bot.log')
else:
    logging.basicConfig(level=logging.INFO)


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
    bot = telegram.Bot(token=TOKEN)
    global LAST_UPDATE_ID

    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    def send(msg: str):
        bot.sendMessage(chat_id=CHAT_ID, text=msg)

    def check_updates(b: telegram.Bot):
        global LAST_UPDATE_ID
        for update in b.getUpdates(
                offset=LAST_UPDATE_ID,
                timeout=INTERVAL,
        ):
            print(update)
            message = update.message.text
            upd_chat_id = update.message.chat_id
            cmd = message.lower()

            if upd_chat_id == CHAT_ID:
                # commands list

                if '/ping' in cmd:
                    send('Pong!')

                elif 'сиськ' in cmd or '/boobs' in cmd:
                    bot.sendPhoto(chat_id=CHAT_ID, photo=get_boobs_url())

                elif 'жоп' in cmd or '/ass' in cmd:
                    bot.sendPhoto(chat_id=CHAT_ID, photo=get_butts_url())

                elif 'курс' in cmd or 'currency' in cmd:
                    send(msg=get_currency())

                elif 'бурик' in cmd:
                    send(msg='https://mvl-private.s3.eu-central-1.amazonaws.com/files/4NLElhE.jpg')

                elif '/ver' in cmd:
                    send(msg=VERSION)

                LAST_UPDATE_ID = update.update_id + 1

            else:
                bot.sendMessage(chat_id=upd_chat_id, text='This Bot not for you :(')
                LAST_UPDATE_ID = update.update_id + 1

    while True:
        try:
            check_updates(bot)
        except KeyboardInterrupt:
            print('Прервано..')
            break
        except Exception as err:
            print(err)
            LAST_UPDATE_ID += 1


@bot_cli.command()
@click.option('-m', '--msg', help='Message to send', type=str)
def send(msg: str):
    """ Send the message into Chat """
    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(chat_id=CHAT_ID, text=msg)


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
