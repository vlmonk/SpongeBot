
FROM ubuntu:trusty

MAINTAINER Egregors (egregors@yandex.ru)

ENV DOCKER 1
ENV TOKEN Dont make this your default
ENV INTERVAL 3
ENV ROOM_ID -10725690

# Set the locale, for ru-lang projects
RUN locale-gen ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

RUN apt-get update && apt-get install -y \
build-essential \
git \
python \
python-dev \
python-setuptools

RUN easy_install pip

ADD . /home/bot/

# RUN pip install
RUN pip install -r /home/bot/requirements.txt

CMD ["python", "/home/bot/src/main.py"]



