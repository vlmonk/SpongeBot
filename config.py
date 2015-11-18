# -*- coding: utf-8 -*-
import os

DOCKER = True if os.environ.get('DOCKER') else False

if DOCKER:
    try:

        TOKEN = os.environ['TOKEN']
        CHAT_ID = int(os.environ['CHAT_ID'])
        INTERVAL = int(os.environ['INTERVAL'])

        print('Interval is: ' + str(INTERVAL))
        print('For token: ' + TOKEN)
        print('For Chat: ' + str(CHAT_ID))
    except:
        raise Exception('INTERVAL ot TOKEN is not defined')

# Put your settings right here
TOKEN = ''
CHAT_ID = None
INTERVAL = 3
