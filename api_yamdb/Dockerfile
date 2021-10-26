

FROM python:3.8.5

LABEL maintainer="Vasil Kovylin" project="YaMDB" version=1

RUN mkdir /code

COPY requirements.txt /code

RUN pip install --upgrade pip && pip3 install -r /code/requirements.txt

COPY . /code

CMD python /code/manage.py runserver 0:8000