# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import time

import requests

requests.packages.urllib3.disable_warnings()  # Disable request ssl warnings

INTERVAL = 3
TOKEN = '112062291:AAHIJsFATg1YiTOZEc0i3e_3a43Gyqalavc'  # Use this token to access the HTTP API
URL = 'https://api.telegram.org/bot'  # HTTP Bot API
offset = 0  # ID lash update
USERS = [567937, 73903140]
# TODO: Написать текст хелпа
HELP_TEXT = 'Здесь будет текст хелпа. Может быть.'


def check_updates():
    """ Check servers updates """
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
            log_event('Unknown update: %s' % update)
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
                name = 'X3'

        if from_id not in USERS:
            send_text("You're not autorized to use me!", from_id)
            log_event('Unautorized: %s' % update)
            continue

        message = update['message']['text']
        parameters = (offset, name, from_id, message)
        log_event('Message (id%s) from %s (id%s): "%s"' % parameters)

        run_command(*parameters)


def log_event(text):
    """
    Процедура логгирования
    ToDo: 1) Запись лога в файл
    """
    event = '{}: {}'.format(time.ctime(), text)
    print(event)


def send_text(chat_id, text):
    """Отправка текстового сообщения по chat_id
    ToDo: повторная отправка при неудаче"""
    log_event('Sending to %s: %s' % (chat_id, text))  # Запись события в лог
    data = {'chat_id': chat_id, 'text': text}  # Формирование запроса
    request = requests.post(URL + TOKEN + '/sendMessage', data=data)  # HTTP запрос
    if not request.status_code == 200:  # Проверка ответа сервера
        return False  # Возврат с неудачей
    return request.json()['ok']  # Проверка успешности обращения к API


def run_command(offset, name, from_id, cmd):
    if cmd == '/ping':
        send_text(from_id, 'pong')
    elif cmd == '/help':
        send_text(from_id, HELP_TEXT)
    else:
        send_text(from_id, 'What do you mean? Use /help')


if __name__ == "__main__":
    print('run')
    while True:
        try:
            check_updates()
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print('Прервано пользователем..')
            break
