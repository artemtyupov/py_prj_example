FROM joyzoursky/python-chromedriver:3.8-selenium

COPY parsing_service/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

COPY parsing_service/*.py /parsing_service/src/
COPY shared_files/*.py /parsing_service/src/shared_files/
COPY shared_files/cookies.pkl /parsing_service/src/shared_files/

CMD [ "python", "/parsing_service/src/main.py" ]