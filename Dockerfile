FROM python:3.8


WORKDIR /chainvote-api

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install  --no-cache-dir  -r requirements.txt

VOLUME /chainvote-api 
ADD /chainvote-api  /chainvote-api