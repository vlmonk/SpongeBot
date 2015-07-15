# SpongeBot — телеграмм-бот для уютной /dev/null. ver: 0.3.1
Небольшой скрипт, который дергает API https://core.telegram.org/bots/api

## Как запустить?
Необходимо указать в conf.py:
* токен для доступа к API
* id пользователей, от которых можно выполнять команды
* интервал, с которым будут проверяться обновления

``` python main.py ```

## Как запустить, используя Docker
* собрать контейнер
``` docker build -t sponge_bot . ```
* запустить контейнер
``` docker run -d -e "TOKEN=BOT_TOKEN" -e "ROOM_ID=12345" --name sponge_bot bot ```
* запустить контейнер, да еще что бы логи было удобно читать
``` docker run -d -e "TOKEN=BOT_TOKEN" -e "ROOM_ID=-12345" -v /path/to/log/:/var/log/sponge/ --name sponge_bot egregors/sponge_bot ```
указав вместо "BOT_TOKEN" токен своего бота, а вместо "12345" id общего чата, где он должен работать.

или просто забрать готовый контейнер с Docker Hub:
``` docker pull egregors/sponge_bot ```

## Что умеет бот?
* Показывать сиськи
* Показывать попки

## Что, вероятно, будет уметь бот?
1. Прогонять картинки через DeepDream
2. Грабить корованы 
3. Переводить китайскую писанину @alexboor

Предложения предлагать в ишьюс. 

## Bot CLI
Еще можно писать от имени бота. Для этого необходимо сделать что-то вроде:
``` python tools/bot.py -T $YOUR TOKEN -c $CHAT_ID -t $TEXT ```