# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import time
import logging

from conf import USERS, URL, TOKEN, HELP_TEXT, DOCKER, ROOM_ID, ADMIN_ID
import requests
from cmd.show_me import show_me_boobs, show_me_butts, show_me_turtle, show_me_currency

requests.packages.urllib3.disable_warnings()  # Disable request ssl warnings
logging.getLogger("requests").setLevel(logging.WARNING)

if DOCKER:
    logging.basicConfig(level=logging.INFO, filename='/var/log/sponge/bot.log')
else:
    logging.basicConfig(level=logging.INFO)

offset = 0  # ID lash update


def check_updates():
    """ Проверка наличия обновлений """
    global offset
    data = {'offset': offset + 1, 'limit': 5, 'timeout': 0}

    try:
        request = requests.post(URL + TOKEN + '/getUpdates', data=data)
    except:
        log_event('Error getting updates', err=True)
        return False

    if not request.status_code == 200: return False
    if not request.json()['ok']: return False
    for update in request.json()['result']:
        offset = update['update_id']

        if not 'message' in update or not 'text' in update['message']:
            log_event('Unknown update: {}'.format(update))
            continue
        from_id = update['message']['chat']['id']

        if int(from_id) > 0:  # приватный чат
            try:
                name = update['message']['chat']['username']
            except:
                name = ''
                if 'first_name' in update['message']['chat']:
                    name += update['message']['chat']['first_name']
                if 'last_name' in update['message']['chat']:
                    name += update['message']['chat']['last_name']
                if not name:
                    name = 'UNKNOWN'
        else:  # групповой чат
            name = update['message']['chat']['title']

        if from_id not in USERS:
            # send_text("You're not autorized to use me!", from_id)
            log_event('Unautorized: {}'.format(update))
            continue

        message = update['message']['text']
        parameters = (offset, name, from_id, message)
        log_event('Message (id%s) from %s (id%s): "%s"' % parameters)

        run_command(*parameters)


def send_text(chat_id, text):
    """ Отправка текстового сообщения по chat_id
    ToDo: повторная отправка при неудаче """
    log_event('Sending to {}: {}'.format(chat_id, text))
    data = {'chat_id': chat_id, 'text': text}
    request = requests.post(URL + TOKEN + '/sendMessage', data=data)
    if not request.status_code == 200:
        return False
    return request.json()['ok']


def send_img():
    pass


def send_file():
    pass


def log_event(text, err=False):
    """ Логирование """
    event = '{}: {}'.format(time.ctime(), text)
    if err:
        logging.error(event)
    else:
        logging.info(event)


def run_command(offset, name, from_id, cmd):
    """
    :param offset: id обновления
    :param name: имя того, кто вызывал команду
    :param from_id: id того, кто вызвал команду
    :param cmd: команда
    :return:

    !IMPORTANT:
    """
    cmd = cmd.lower()
    if '/ping' in cmd:
        send_text(from_id, 'pong')

    elif '/help' in cmd:
        send_text(from_id, HELP_TEXT)

    elif 'сиськ' in cmd or '/boobs' in cmd:
        boobs = show_me_boobs()
        if boobs:
            send_text(from_id, boobs)
        else:
            send_text(from_id, 'Что-то пошло не так.')

    elif 'жоп' in cmd or '/ass' in cmd:
        butts = show_me_butts()
        if butts:
            send_text(from_id, butts)
        else:
            send_text(from_id, 'Что-то пошло не так.')

    elif 'бурик' in cmd:
        send_text(from_id, show_me_turtle())

    elif 'курс' in cmd or 'currency' in cmd:
        send_text(from_id, show_me_currency())

    elif '/bot_say ' in cmd and from_id is ADMIN_ID:
        print ('admin say!')
        send_text(ROOM_ID, cmd.replace('/bot_say ', ''))

    else:
        pass
