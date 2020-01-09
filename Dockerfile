FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /home/slack_bot
ADD requirements.txt /home/slack_bot/
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
        ;
RUN pip install -r requirements.txt
ADD . /home/slack_bot/
EXPOSE 9001
