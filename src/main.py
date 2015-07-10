# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import time

from conf import INTERVAL
from core import check_updates

if __name__ == "__main__":
    while True:
        try:
            check_updates()
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print('Прервано пользователем..')
            break
        # except Exception:
        #     print('Что-то пошло не так..')
