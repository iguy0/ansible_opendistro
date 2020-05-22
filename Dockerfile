FROM python:slim

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /code
CMD /bin/bash
