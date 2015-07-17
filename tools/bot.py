# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import click
import requests


@click.command()
@click.option('-T', '--token', help='Your Telegram API TOKEN', prompt='Your API token')
@click.option('-c', '--chat_id', default=-10725690, help='ID of target Chat', prompt='ID of target Chat')
@click.option('-t', '--text', help='text to send', prompt='Text to send')
@click.option('-i', '--interactive', help='', is_flag=True, default=False)
def send(token, chat_id, text, interactive):
    data = {'chat_id': chat_id, 'text': text}
    request = requests.post('https://api.telegram.org/bot' + token + '/sendMessage', data=data)
    print('bot: OK') if request.status_code == 200 else print('bot: FAILED')

    if interactive:
        print('To exit press CTRL + C')
        status = '[last msg status..]'
        while True:
            try:
                t = input(status + ' TEXT: ')
                data = {'chat_id': chat_id, 'text': t}
                request = requests.post('https://api.telegram.org/bot' + token + '/sendMessage', data=data)
            except Exception as err:
                status = '[FAILED: ' + str(err) + ']'
                print(status)

            if request.status_code == 200:
                status = '[OK]'
            else:
                status = '[FAILED]'


if __name__ == '__main__':
    send()
