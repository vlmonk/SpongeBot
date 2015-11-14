# -*- coding: utf-8 -*-
#
#   bot_d
#   =====
#   ver.: 2.0
#
#   «Я видел некоторое дерьмо»
#                       Букля.
#
#   @SpongeBot
#   ~~~~~~~~~~
#   Демон для работы с API бота для уютного чатика «/dev/null»
#   Умеет много всякого. И продолжает учиться. В отличии от тебя.
#
#
#
#
#
#
#   (с) @egregors 2015

from __future__ import unicode_literals

import click
import telegram
from config import CHAT_ID, INTERVAL, TOKEN

@click.group()
@click.command()
@click.option('-T', '--token', expose_value=False,
              default=TOKEN,
              help='Telegram Bot API token',
              prompt='API token',
              type=str)
@click.option('-c', '--chat_id',
              default=CHAT_ID,
              help='ID of target Chat',
              prompt='ID of target Chat',
              type=int)
@click.option('-i', '--interval',
              default=INTERVAL,
              help='API updates check timeout',
              prompt='Update timeout',
              type=int)
def start(token, chat_id, interval):
    bot = telegram.Bot(token=token)
    global LAST_UPDATE_ID

    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    def check_updates(b: telegram.Bot):
        global LAST_UPDATE_ID
        for update in b.getUpdates(
                offset=LAST_UPDATE_ID,
                timeout=interval,
        ):
            print(update)

    while True:
        try:
            check_updates(bot)
        except KeyboardInterrupt:
            print('Прервано..')
            break


if __name__ == '__main__':
    start()
