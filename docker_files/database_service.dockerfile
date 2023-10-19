FROM python:3.9-alpine as builder

COPY database_service/requirements.txt /tmp/requirements.txt

# install psycopg2 dependencies
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN python3 -m pip install -r /tmp/requirements.txt

COPY database_service/*.py /database_service/src/
COPY shared_files/*.py /database_service/src/shared_files/

CMD [ "python", "/database_service/src/main.py" ]