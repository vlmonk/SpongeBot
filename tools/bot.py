import click
import requests


@click.command()
@click.option('-T', '--token', help='Your Telegram API TOKEN', prompt='Your API token')
@click.option('-c', '--chat_id', default=-10725690, help='ID of target Chat', prompt='ID of target Chat')
@click.option('-t', '--text', help='text to send', prompt='Text to send')
def send(token, chat_id, text):
    data = {'chat_id': chat_id, 'text': text}
    request = requests.post('https://api.telegram.org/bot' + token + '/sendMessage', data=data)
    print('bot: done') if request.status_code == 200 else print('bot: fail')


if __name__ == '__main__':
    send()
