
FROM ubuntu:trusty

MAINTAINER Egregors (egregors@yandex.ru)

ENV DOCKER 1

# Set the locale, for ru-lang projects
RUN locale-gen ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

RUN apt-get update && apt-get install -y \
git \
python3 \
libcurl4-openssl-dev \
libxml2-dev \
libxslt1-dev \
python-dev

RUN apt-get install -y python3-pip

# install requirements
ADD requirements.txt /home/bot/requirements.txt
RUN pip3 install -r /home/bot/requirements.txt

ADD . /home/bot/

VOLUME ["/var/log/sponge"]

CMD ["python3", "/home/bot/bot_d.py", "start"]
