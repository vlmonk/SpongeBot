# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

from conf import USERS, URL, TOKEN, HELP_TEXT
import requests

requests.packages.urllib3.disable_warnings()  # Disable request ssl warnings

offset = 0  # ID lash update

def check_updates():
    """ Проверка наличия обновлений """
    global offset
    data = {'offset': offset + 1, 'limit': 5, 'timeout': 0}

    try:
        request = requests.post(URL + TOKEN + '/getUpdates', data=data)
    except:
        log_event('Error getting updates')
        return False

    if not request.status_code == 200: return False
    if not request.json()['ok']: return False
    for update in request.json()['result']:
        offset = update['update_id']

        if not 'message' in update or not 'text' in update['message']:
            log_event('Unknown update: {}'.format(update))
            continue
        from_id = update['message']['chat']['id']

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

        if from_id not in USERS:
            # send_text("You're not autorized to use me!", from_id)
            log_event('Unautorized: {}'.format(update))
            continue

        message = update['message']['text']
        parameters = (offset, name, from_id, message)
        log_event('Message (id%s) from %s (id%s): "%s"' % parameters)

        run_command(*parameters)


def log_event(text):
    """ Логирование
    ToDo: 1) Запись лога в файл \ db \ еще куда-нибудь """
    event = '{}: {}'.format(time.ctime(), text)
    print(event)


def send_text(chat_id, text):
    """ Отправка текстового сообщения по chat_id
    ToDo: повторная отправка при неудаче """
    log_event('Sending to {}: {}'.format(chat_id, text))
    data = {'chat_id': chat_id, 'text': text}
    request = requests.post(URL + TOKEN + '/sendMessage', data=data)
    if not request.status_code == 200:
        return False
    return request.json()['ok']


def run_command(offset, name, from_id, cmd):
    if cmd == '/ping':
        send_text(from_id, 'pong')
    elif cmd == '/help':
        send_text(from_id, HELP_TEXT)
    else:
        send_text(from_id, 'Ты кто такой? Давай, до свиданья! /help')
