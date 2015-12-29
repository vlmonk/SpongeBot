# -*- coding: utf-8 -*-
import os

DOCKER = True if os.environ.get('DOCKER') else False

if DOCKER:
    try:

        TOKEN = os.environ['TOKEN']
        CHAT_ID = [int(x) for x in str(os.environ['CHAT_ID']).split(' ')]
        INTERVAL = int(os.environ['INTERVAL'])

        print('Interval is: ' + str(INTERVAL))
        print('For token: ' + TOKEN)
        print('For Chat: ')
        print(CHAT_ID)
    except Exception as err:
        print(err)
else:
    # Put your settings right here
    TOKEN = ''
    CHAT_ID = None
    INTERVAL = 3
