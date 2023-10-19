FROM python:3.9-alpine as builder

COPY excel_service/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

COPY excel_service/*.py /excel_service/src/
COPY excel_service/templates/*.xlsx /excel_service/src/templates/
COPY shared_files/*.py /excel_service/src/shared_files/

CMD [ "python", "/excel_service/src/main.py" ]