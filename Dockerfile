FROM python:3.7
MAINTAINER Sreenadh TC "kesav.tc8@gmail.com"

ENV CONTACTS_ENV=production
ENV FLASK_APP=run.py

COPY ./contacts /contacts-app/contacts
COPY ./migrations ./contacts-app/migrations
COPY ./scripts ./contacts-app/scripts
COPY ./requirements.txt ./contacts-app/
COPY ./run.py ./contacts-app/

WORKDIR /contacts-app

RUN pip install -r requirements.txt

CMD /contacts-app/scripts/run