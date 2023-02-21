FROM python:3.7-alpine

#COMMANDS FOR FFMPEG
RUN apk update && apk add ffmpeg

# Install Docker
RUN apk update && \
    apk add docker


ENV PATH="/usr/local/bin:${PATH}"

ENV PYTHONUNBUFFERED 1

RUN pip install selenium
RUN pip install beautifulsoup4
#RUN pip install subprocess


RUN pip3 install google-cloud-storage
RUN pip install --upgrade google-cloud-storage
RUN pip3 install google-auth
RUN pip3 install google-auth-oauthlib
RUN pip3 install google-auth-httplib2


RUN pip install --upgrade google-api-python-client
RUN pip3 install google-auth google-auth-oauthlib
RUN pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
RUN pip install --upgrade google-api-python-client

RUN mkdir /app
COPY ./app /app
WORKDIR /app