FROM python:3.13-alpine

WORKDIR /usr/app

COPY . .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
RUN apk update && apk add --no-cache firefox