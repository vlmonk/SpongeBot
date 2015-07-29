# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

__author__ = 'egregors'

DOCKER = True if os.environ.get('DOCKER') else False

# USERS = [-10725690, ]  # id пользователей, от которых можно выполнять команды
USERS = [567937, 73903140, 113381144, 101330553]  # id пользователей, от которых можно выполнять команды
# egre, green. unreal, harald

USERS.append(-23141912) # Пикник

if DOCKER:
    try:
        INTERVAL = int(os.environ['INTERVAL'])
        TOKEN = os.environ['TOKEN']
        USERS.append(int(os.environ['ROOM_ID']))

        print('Interval is: ' + str(INTERVAL))
        print('For token: ' + TOKEN)
        print('For users or groups: ')
        print(USERS)
    except:
        raise Exception('INTERVAL ot TOKEN is not defined')
else:
    INTERVAL = 1
    TOKEN = ''  # Токен для доступа к API

URL = 'https://api.telegram.org/bot'  # HTTP Bot API

HELP_TEXT = \
    """
    Здесь будет текст хелпа. Может быть.
    *   *   *
    # Команды:
    /help - показать это бесполезное сообщение
    /ping - понг
    /boobs - показать сиськи
    /ass — показать попку

    # Упоменания
    сиськи - показать сиськи
    жопа - показать попку
    бурик — показать черепаху, похожую на Бурика

    Потыкай меня палкой: https://github.com/Egregors/SpongeBot
    """
