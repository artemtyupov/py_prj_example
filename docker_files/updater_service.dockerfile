FROM python:3.9-alpine as builder

COPY updater_service/requirements.txt /tmp/requirements.txt

RUN python3 -m pip install -r /tmp/requirements.txt

COPY updater_service/*.py /updater_service/src/
COPY shared_files/*.py /updater_service/src/shared_files/

CMD [ "python", "/updater_service/src/main.py" ]