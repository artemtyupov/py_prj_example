FROM python:3.9-alpine as builder

COPY tg_bot/requirements.txt /tmp/requirements.txt

RUN python3 -m pip install -r /tmp/requirements.txt

COPY tg_bot/*.py /tg_bot_service/src/
COPY shared_files/*.py /tg_bot_service/src/shared_files/
COPY shared_files/cookies.pkl /parsing_service/src/shared_files/

CMD [ "python", "/tg_bot_service/src/main.py" ]