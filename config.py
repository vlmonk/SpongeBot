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
TOKEN = '112062291:AAHhOtR7FxNGVYbi9PTHTntPKxpe_fvpdAQ'
CHAT_ID = -10725690
INTERVAL = 3
